# Skin Intelligence: technical approach

## Product workflow

1. The user registers and signs in with a JWT.
2. They complete their skin profile, lifestyle, environment, and sleep inputs.
3. The assessment engine ranks concerns and adds lifestyle, sleep, and environmental risk factors.
4. The routine generator creates morning, evening, weekly, and recommendation lists.
5. The dashboard shows the skin-health score and the next required action.

This implements the PDF's Milestone 1–2 workflow: profile management, assessment and concern analysis, routine generation, recommendations, and weighted skin scoring. Ingredient intelligence, product recommendations, progress analytics, reporting, and deployment remain Milestones 3–4.

## Frontend approach

- React + React Router provides protected, task-focused pages.
- `AppShell` provides the authenticated workspace navigation model; existing data-entry pages retain their focused back-to-dashboard header while the workflow is being incrementally consolidated.
- Native forms provide validation, loading states, and human-readable feedback.
- The dashboard is workflow-first: complete profile data before assessment, and assessment before routine generation.

## API approach

- The browser sends the JWT as `Authorization: Bearer <token>`.
- FastAPI remains the source of truth; the frontend does not use mock health, routine, or assessment data.
- Missing optional data is presented as an incomplete setup step, not a generic error.

## Production hardening next

- Move API URLs and secrets to environment variables.
- Use secure HttpOnly cookies or a hardened token-storage strategy.
- Add client/API tests, schema validation, audit logging, rate limits, and monitoring.
- Add role-specific screens only after the consultant and dermatologist APIs are implemented.
