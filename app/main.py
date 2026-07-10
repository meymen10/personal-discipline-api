from fastapi import FastAPI, status
from app.schemas import WorkoutCreate, MealCreate
from datetime import time

app = FastAPI(
    title="Personal Discipline and Performance API",
    description="Backend service for tracking workouts, swimming sessions, and time-restricted feeding routines.",
    version="1.0.0"
)

# In-memory storage (Temporary before database integration)
db_workouts = []
db_meals = []

@app.get("/", tags=["General"])
def read_root():
    return {"status": "System online", "version": "1.0.0-alpha"}

@app.post("/workouts/", status_code=status.HTTP_201_CREATED, tags=["Workouts"])
def log_workout(workout: WorkoutCreate):
    db_workouts.append(workout)
    return {"message": "Workout logged successfully", "data": workout}

@app.get("/workouts/", tags=["Workouts"])
def get_workouts():
    return {"total_count": len(db_workouts), "records": db_workouts}

@app.post("/meals/", status_code=status.HTTP_201_CREATED, tags=["Nutrition"])
def log_meal(meal: MealCreate):
    # Strict intermittent fasting rule: warn if meal is logged after 17:00 (5:00 PM)
    limit_time = time(17, 0)
    is_late = meal.log_time > limit_time
    
    meal_data = meal.model_dump()
    meal_data["intermittent_fasting_violation"] = is_late
    
    db_meals.append(meal_data)
    
    if is_late:
        return {
            "message": "Meal logged BUT the 17:00 time limit was exceeded!",
            "status": "Time Limit Violation",
            "data": meal_data
        }
        
    return {"message": "Meal logged successfully within the time restrictions", "data": meal_data}

@app.get("/meals/", tags=["Nutrition"])
def get_meals():
    return {"total_count": len(db_meals), "records": db_meals}