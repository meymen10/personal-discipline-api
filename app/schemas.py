from pydantic import BaseModel, Field
from datetime import time
from typing import Optional, List

# --- WORKOUT MODELS ---
class WeightLog(BaseModel):
    exercise_name: str = Field(..., examples=["Shoulder Press"])
    equipment: str = Field(..., examples=["Dumbbells"])  # Yeni alan eklendi
    sets: int = Field(..., gt=0, examples=[4])
    reps: int = Field(..., gt=0, examples=[10])
    weight_kg: float = Field(..., gt=0, examples=[15.0])

class SwimmingLog(BaseModel):
    distance_meters: int = Field(..., gt=0, examples=[1500])
    duration_minutes: int = Field(..., gt=0, examples=[45])
    style: str = Field(..., examples=["Freestyle"])

class WalkingLog(BaseModel):
    distance_km: float = Field(..., gt=0, examples=[6.0])
    duration_minutes: int = Field(..., gt=0, examples=[60])
    location: str = Field(..., examples=["Outdoor/Park"])
    # --- YENİ EKLENEN DIŞ API ALANLARI ---
    temperature_c: Optional[float] = Field(default=None, description="Otomatik olarak dış API'den çekilecek")
    weather_condition: Optional[str] = Field(default=None, description="Otomatik olarak dış API'den çekilecek")

class WorkoutCreate(BaseModel):
    workout_type: str = Field(..., examples=["Weightlifting", "Swimming", "Walking"])
    weight_details: Optional[List[WeightLog]] = None
    swimming_details: Optional[SwimmingLog] = None
    walking_details: Optional[WalkingLog] = None

# --- HYDRATION MODEL (YENİ) ---
class HydrationLog(BaseModel):
    amount_ml: int = Field(..., gt=0, examples=[500])
    is_cold: bool = Field(True, examples=[True])
    infused_with: Optional[List[str]] = Field(default=[], examples=[["lemon", "mint"]])

# --- NUTRITION MODELS ---
class MealCreate(BaseModel):
    meal_name: str = Field(..., examples=["Dinner"])
    calories: int = Field(..., gt=0, examples=[650])
    log_time: time = Field(..., examples=["16:30:00"])
    contains_refined_sugar: bool = Field(False, examples=[False]) # Yeni kural alanı eklendi