from pydantic import BaseModel, Field
from datetime import time
from typing import Optional, List

# --- WORKOUT MODELS ---
class WeightLog(BaseModel):
    exercise_name: str = Field(..., examples=["Bench Press"])
    sets: int = Field(..., gt=0, examples=[4])
    reps: int = Field(..., gt=0, examples=[10])
    weight_kg: float = Field(..., gt=0, examples=[80.0])

class SwimmingLog(BaseModel):
    distance_meters: int = Field(..., gt=0, examples=[1500])
    duration_minutes: int = Field(..., gt=0, examples=[45])
    style: str = Field(..., examples=["Freestyle"])

class WalkingLog(BaseModel):
    distance_km: float = Field(..., gt=0, examples=[6.5])
    duration_minutes: int = Field(..., gt=0, examples=[75])
    location: str = Field(..., examples=["Outdoor/Park"])

class WorkoutCreate(BaseModel):
    workout_type: str = Field(..., examples=["Weightlifting", "Swimming", "Walking"])
    weight_details: Optional[List[WeightLog]] = None
    swimming_details: Optional[SwimmingLog] = None
    walking_details: Optional[WalkingLog] = None

# --- NUTRITION MODELS ---
class MealCreate(BaseModel):
    meal_name: str = Field(..., examples=["Dinner"])
    calories: int = Field(..., gt=0, examples=[650])
    log_time: time = Field(..., examples=["16:30:00"])