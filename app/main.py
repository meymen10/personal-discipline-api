from fastapi import FastAPI, status
from app.schemas import WorkoutCreate, MealCreate, HydrationLog
from datetime import time

app = FastAPI(
    title="Personal Discipline and Performance API",
    description="Backend service for tracking workouts, hydration, and strict dietary routines.",
    version="1.1.0"
)

db_workouts = []
db_meals = []
db_hydration = [] # Yeni geçici veri tabanı

@app.get("/", tags=["General"])
def read_root():
    return {"status": "System online", "version": "1.1.0"}

# --- WORKOUT ENDPOINTS ---
@app.post("/workouts/", status_code=status.HTTP_201_CREATED, tags=["Workouts"])
async def log_workout(workout: WorkoutCreate): # YENİ: async eklendi
    
    # EĞER BİR YÜRÜYÜŞ KAYDI VARSA DIŞ API'YE (OPEN-METEO) BAĞLAN
    if workout.walking_details:
        # İstanbul Koordinatları
        weather_url = "https://api.open-meteo.com/v1/forecast?latitude=41.01&longitude=28.97&current_weather=true"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(weather_url)
                if response.status_code == 200:
                    weather_data = response.json().get("current_weather", {})
                    # Dışarıdan gelen veriyi kendi şemamıza yazdırıyoruz
                    workout.walking_details.temperature_c = weather_data.get("temperature")
                    workout.walking_details.weather_condition = f"Rüzgar: {weather_data.get('windspeed')} km/h"
            except Exception:
                # Dış API çökerse bizim sistemimiz hata vermesin, sadece bilgi düşsün
                workout.walking_details.weather_condition = "Dış API'ye ulaşılamadı"

    db_workouts.append(workout)
    return {"message": "Workout logged successfully", "data": workout}

@app.get("/workouts/", tags=["Workouts"])
def get_workouts():
    return {"total_count": len(db_workouts), "records": db_workouts}

# --- HYDRATION ENDPOINTS (YENİ) ---
@app.post("/hydration/", status_code=status.HTTP_201_CREATED, tags=["Hydration"])
def log_hydration(hydration: HydrationLog):
    db_hydration.append(hydration)
    return {"message": "Hydration details logged", "data": hydration}

@app.get("/hydration/", tags=["Hydration"])
def get_hydration():
    return {"total_count": len(db_hydration), "records": db_hydration}

# --- NUTRITION ENDPOINTS ---
@app.post("/meals/", status_code=status.HTTP_201_CREATED, tags=["Nutrition"])
def log_meal(meal: MealCreate):
    limit_time = time(17, 0)
    is_late = meal.log_time > limit_time
    has_sugar = meal.contains_refined_sugar
    
    meal_data = meal.model_dump()
    meal_data["intermittent_fasting_violation"] = is_late
    meal_data["sugar_violation"] = has_sugar
    
    db_meals.append(meal_data)
    
    warnings = []
    if is_late:
        warnings.append("Time Limit (17:00) Exceeded")
    if has_sugar:
        warnings.append("Refined Sugar Detected")
        
    if warnings:
        return {
            "message": "Meal logged BUT rule violations occurred!",
            "status": " | ".join(warnings),
            "data": meal_data
        }
        
    return {"message": "Meal logged successfully within all discipline rules", "data": meal_data}

@app.get("/meals/", tags=["Nutrition"])
def get_meals():
    return {"total_count": len(db_meals), "records": db_meals}