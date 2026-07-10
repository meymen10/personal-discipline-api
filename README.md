# Personal Discipline and Performance API

A modern, high-performance RESTful backend service built with **FastAPI** for tracking daily physical disciplines and dietary constraints.

## 🚀 Features

- **Workout Tracking:** Logs detailed metrics for weightlifting (sets, reps, weight) and swimming sessions (distance, duration, style).
- **Strict Nutrition Management:** Implements a time-restricted feeding business rule, returning specific alerts or violation flags if meals are logged after the 17:00 (5:00 PM) daily cutoff.
- **Auto-generated Documentation:** Interactive Swagger UI provided out-of-the-box by FastAPI.

## 🛠️ Tech Stack

- **Python 3+**
- **FastAPI** (Web framework)
- **Uvicorn** (ASGI server)
- **Pydantic** (Data validation)

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/personal-discipline-api.git](https://github.com/YOUR_USERNAME/personal-discipline-api.git)
   cd personal-discipline-api
