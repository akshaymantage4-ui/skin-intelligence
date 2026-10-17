# AI Skin Intelligence & Personalized Skincare — M1 + M2 + M3

This package starts from the supplied M1/M2 project and completes **Milestone 3 (Week 5–6)** from the project specification.

## Milestone 3 implemented

1. Ingredient intelligence engine
   - Ingredient lookup and function
   - Reference flags: fragrance, EU allergen, comedogenicity, fungal-acne-trigger, pregnancy-caution
   - Basic routine interaction notes
   - Saved ingredient-analysis history in PostgreSQL
2. Product recommendation workflow
   - Product catalog stored in PostgreSQL
   - Skin-type and concern matching
   - Budget filtering
   - Category filtering
   - Suitability score and explanation reasons
   - Saved recommendation requests/results in PostgreSQL
3. Progress tracking
   - Dated skin score entries
   - Routine adherence
   - Notes
   - Saved progress records in PostgreSQL
4. Analytics
   - Latest score
   - First-to-latest change
   - Trend label
   - Average/latest routine adherence
   - Progress timeline
   - Recommendation activity counts
5. User dashboard
   - Existing M1/M2 workflow remains
   - New M3 navigation for Ingredients, Products, Progress and Analytics

## Tech stack from the supplied PDF

Backend: Python + FastAPI
Frontend: JavaScript + React.js
Database: PostgreSQL (primary); MongoDB is listed in the specification as a secondary option, but M1–M3 persistence in this package uses PostgreSQL.
AI/ML libraries: scikit-learn, TensorFlow, PyTorch, Pandas, NumPy (the M3 implementation uses Pandas for the ingredient reference workflow; no paid API is required).
Recommendation/analytics: rule-based recommendation workflow + scoring/analytics; the PDF lists XGBoost, LightGBM and recommendation models as possible technologies.
Cloud/DevOps: Docker, AWS/Azure (Milestone 4 scope; not required to run M3 locally).
Libraries/frameworks: FastAPI, React.js, Next.js, Tailwind CSS, JWT Authentication, Chart.js, Plotly (the current local dashboard uses React and Recharts for the trend chart).
Development tools: VS Code, Git/GitHub, Docker Compose, GitHub Actions, Postman.

## Run in VS Code

### 1. PostgreSQL
Create a database named `skin_intelligence` in PostgreSQL/pgAdmin.

### 2. Backend
Open a terminal in `backend`:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and put your PostgreSQL password.

Then:

```powershell
python database.py
uvicorn main:app --reload
```

Backend: http://127.0.0.1:8000
Swagger: http://127.0.0.1:8000/docs

### 3. Frontend
Open a second VS Code terminal in `skin-intelligence-frontend`:

```powershell
npm install
npm run dev
```

Frontend: http://localhost:5173

## Database behavior

`Base.metadata.create_all()` creates the M1–M3 tables that are missing. It does not delete existing M1/M2 data.

On startup the backend also seeds the product catalog only when the `products` table is empty.

## M3 API endpoints

- `POST /user/ingredients/analyze`
- `POST /user/ingredients/suitability`
- `GET /user/ingredients/history`
- `GET /user/products`
- `POST /user/products/recommendations`
- `GET /user/products/recommendation-history`
- `POST /user/progress`
- `GET /user/progress`
- `DELETE /user/progress/{progress_id}`
- `GET /user/analytics/dashboard`

All M3 user endpoints require the JWT returned by `/auth/login`.

## 20-loop verification

After both servers are running and a test user can log in, run:

```powershell
python verify_m3_20_loops.py
```

The script performs the complete M3 API workflow repeatedly and checks that PostgreSQL-backed records are returned. It is intentionally included so the final local verification happens against **your actual PostgreSQL instance**, which this development environment cannot access.

## Important safety note

Ingredient and product outputs are software reference/recommendation features, not medical diagnoses or guarantees of individual safety. Persistent or severe skin concerns should be evaluated by a qualified dermatologist.
- `POST /user/products/compare`
- `GET /user/products/{product_id}/alternatives`
- `GET /user/progress/comparison`
