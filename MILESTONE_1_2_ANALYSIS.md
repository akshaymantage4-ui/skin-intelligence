# Milestone 1–2 Architecture and Delivery Analysis

## Executive conclusion

The PDF describes a four-milestone platform, not a requirement to deliver all modules in Weeks 1–4. Milestone 1 establishes the application foundation and health-data inputs. Milestone 2 turns those inputs into an explainable assessment, a personalized routine, recommendations, and a weighted score. A rule-based decision engine is sufficient for these two milestones; trained ML, ingredient intelligence, product recommendation, trend analysis, reporting, and cloud deployment are explicitly later work.

The current project substantially covers the functional Milestone 1–2 user path. It is **demo-ready**, but it is not production-ready and it does not yet implement the full role-based architecture or genuine ML promised by the target-state product vision.

## 1. Architecture in the PDF

The PDF names the following logical layers. It does not provide a detailed component or sequence diagram on the extracted architecture page, so this is a faithful interpretation of the stated modules rather than an invented diagram.

```text
React client
  └─ Authentication and role-aware user experience
      └─ FastAPI application
          ├─ Identity and user profiles
          ├─ Skin/lifestyle/environment/sleep data capture
          ├─ Assessment and scoring services
          ├─ Routine and recommendation services
          ├─ Ingredient and product intelligence (later)
          ├─ Progress, analytics, reporting (later)
          └─ Notification and export services (later)
              └─ Persistent data stores and external knowledge/data sources
```

The intended data flow is:

```text
Profile + lifestyle + sleep + environment + reported concerns
       → assessment / risk analysis
       → concern priorities + skin-health score
       → personalized routine + recommendations
       → later: adherence/progress/product feedback loop
```

The score must use these weights: skin condition 35%, lifestyle 20%, sleep 15%, routine consistency 20%, and hydration 10%. [1]

## 2. Exact Milestone 1 requirements

The document defines Milestone 1 as Weeks 1–2: “Project Initialization, Design Process & Core Setup.” [2]

| Requirement | Meaning in the product | Current project status | Evidence / gap |
|---|---|---:|---|
| Define objectives and skincare workflows | Identify the user journey from data collection to advice | Partial | The workflow exists in code and UI; formal wireframes/requirements are not stored in the repository. |
| System architecture and database schema | Establish frontend, API, data entities, and service boundaries | Partial | React, FastAPI, PostgreSQL models, routes, and services exist. No migrations or formal architecture diagram exist. |
| Frontend and backend setup | Runnable React client and FastAPI server | Complete for local development | Vite frontend and FastAPI backend build/run locally. |
| Authentication and role-based access | Register, login, JWT/OAuth2, user/consultant/dermatologist/admin access | Partial | Registration, password hashing, JWT login, and protected endpoints work. User role is stored but not authorized by role; OAuth provider login and role dashboards are absent. |
| Skin profile workflow | Capture skin type and concerns | Complete for baseline user workflow | Skin type plus acne, dryness, pigmentation, and sensitivity are stored. |
| Lifestyle and sleep tracking | Capture habits that influence recommendations | Complete for baseline user workflow | Lifestyle values and dated sleep logs exist. |
| Hydration and environmental exposure | Capture water intake, UV/pollution/climate inputs | Complete for baseline user workflow | Water is in lifestyle; environment profile captures UV, pollution, temperature, humidity, and water quality. |

### Milestone 1 data-model observations

The PDF also lists age group, allergies, and sensitivities as skin information. [3] The repository has a generic profile with age and gender, and a skin profile with sensitivity. It does **not** yet persist age group, a structured allergy list, or product/ingredient sensitivities. Those omissions do not prevent the core Weeks 1–2 path, but they must be added before ingredient suitability or allergy detection can be trustworthy.

## 3. Exact Milestone 2 requirements

The document defines Milestone 2 as Weeks 3–4: “Skin Assessment & Routine Generation.” [2]

| Requirement | Acceptance behavior | Current project status | Gap to close |
|---|---|---:|---|
| Skin assessment engine | Convert user-reported condition levels into understandable results | Complete, rule-based | It is not an ML classifier and cannot analyze photos or clinical evidence. |
| Skin concern analysis | Identify concerns, prioritize them, and identify risk factors | Complete for acne, dryness, pigmentation, and sensitivity | Add dark spots, redness, fine lines, wrinkles, uneven tone, and oily-skin concern support if the full PDF concern list is required. |
| Personalized routine generation | Generate morning, evening, weekly, and recommendations | Complete at a baseline | Seasonal recommendations and adaptive updates are listed in the module description but not built. |
| Skin scoring workflow | Produce the defined weighted score | Partially complete | The five score buckets match the weights, but “routine consistency” currently means a routine exists, not adherence. Stress threshold is inconsistent with the UI scale. |
| Recommendations | Provide actionable, personalized skincare guidance | Complete at a baseline | Guidance is generic; it is not an ingredient or product recommendation engine. |

The stated Milestone 2 outcomes are: assessment engine operational, routine generation functional, and scoring system completed. [2] The project satisfies those outcomes for a questionnaire-driven proof of concept.

## 4. What is and is not AI/ML

### Completed intelligence approach

The assessment service is deterministic rules: concern severity is mapped to a priority, and lifestyle, sleep, and environmental thresholds append risk factors. The routine service chooses conservative steps based on the selected concern levels and lifestyle input. This is **explainable decision logic**, which is appropriate for early validation because every output has a visible rule and no unsupported medical prediction is implied.

### Not completed ML

The PDF’s target platform mentions AI-powered assessment, ingredient intelligence, product recommendation, analytics, and later libraries such as scikit-learn, TensorFlow, PyTorch, XGBoost, and LightGBM. [1][4] None of those models, datasets, feature pipelines, evaluations, training scripts, or inference endpoints exist in the current repository. Therefore the product must not be represented as having trained ML or clinical diagnostic capability.

## 5. Required workflow for a correct Milestone 1–2 demo

1. Register and log in.
2. Complete the skin profile.
3. Enter lifestyle data, including water, sleep, stress, and sun exposure.
4. Add at least one dated sleep log.
5. Add environmental exposure data where available.
6. Submit the skin assessment.
7. Review concern priorities, risk factors, and the safety disclaimer.
8. Generate a routine.
9. View the score and its five components on the dashboard.

This ordering matters: missing profile data should be presented as a setup step, not silently treated as healthy data. The redesigned dashboard follows this order.

## 6. Architecture decisions for the next implementation pass

### Must fix before calling the system production-ready

1. Move database credentials, JWT secret, and API base URL out of source code into environment configuration.
2. Add Alembic database migrations and database constraints ensuring one active profile/assessment/routine per user where intended.
3. Enforce roles with authorization dependencies; do not rely only on a `role` column.
4. Add automated API, service, and browser-flow tests.
5. Add rate limiting, structured logs, error monitoring, validation ranges, and audit trails.
6. Use secure token handling and HTTPS in deployment.
7. Require human/dermatologist escalation for severe or persistent concerns; retain non-diagnostic language.

### Required to complete the PDF’s later target state

| Milestone | Build next | Core technical work |
|---|---|---|
| 3 | Ingredient intelligence | Structured ingredient catalog; user allergy/sensitivity model; suitability/interaction rule engine; evidence sources. |
| 3 | Product recommendations | Normalized product catalog; eligibility filters; transparent scoring/ranking; budget and availability inputs. |
| 3 | Progress tracking | Dated assessments, routine-adherence events, trend calculations, and consented photo handling if used. |
| 4 | Analytics and reports | Role-specific dashboards, exports, report templates, and metrics. |
| 4 | Deployment | Docker, secrets manager, CI/CD, managed database, monitoring, backups, security review. |
| Future ML | ML only after data readiness | Define labels, consent, data quality, bias evaluation, offline metrics, versioned models, and human oversight before inference. |

## 7. Recommended definition of done

For **Milestone 1**, call it done only when a new user can register, authenticate, save profile/lifestyle/environment data, create sleep logs, and reload those records after signing in.

For **Milestone 2**, call it done only when the required demo workflow runs from fresh account to score and routine, every result is persisted, the score totals 100 with the stated weights, and validation/error states are tested. The current implementation meets the main functional path, but needs automated end-to-end coverage and the production hardening items above before it is operationally production-ready.

## Sources

1. *AI Skin Intelligence & Personalized Skincare Planner*, provided PDF, pp. 4–7. Accessed locally. Used for routine categories, scoring weights, analytics/dashboard target state, and later modules.
2. *AI Skin Intelligence & Personalized Skincare Planner*, provided PDF, pp. 8–10. Accessed locally. Used for Week 1–4 tasks, outcomes, and the Milestone 3–4 boundary.
3. *AI Skin Intelligence & Personalized Skincare Planner*, provided PDF, p. 3. Accessed locally. Used for the specified skin-information fields and assessment-engine scope.
4. *AI Skin Intelligence & Personalized Skincare Planner*, provided PDF, pp. 11–13. Accessed locally. Used for the stated technology, ML, and deployment targets.
