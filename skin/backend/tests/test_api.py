
from datetime import date
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from main import app
from database import SessionLocal
from models.user import User

client = TestClient(app)




@pytest.fixture
def test_user():
    from routes.auth import pwd_context

    email = f"test_{uuid4().hex}@example.com"
    password = "TestPassword123!"

    db = SessionLocal()

    try:
        user = User(
            name="Test User",
            email=email,
            password=pwd_context.hash(password),
            role="user",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_data = {
            "id": user.id,
            "email": email,
            "password": password,
        }

    finally:
        db.close()

    try:
        yield user_data

    finally:
        cleanup_db = SessionLocal()
        try:
            saved_user = (
                cleanup_db.query(User)
                .filter(User.email == email)
                .first()
            )

            if saved_user:
                cleanup_db.delete(saved_user)
                cleanup_db.commit()
        finally:
            cleanup_db.close()



def get_auth_token(email, password):
    """
    Log in and return a bearer token.
    """
    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
    )

    assert response.status_code == 200, response.text

    return response.json()["access_token"]


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Skin Intelligence API is running"


def test_analytics_requires_authentication():
    response = client.get("/user/analytics/dashboard")

    assert response.status_code in (401, 403)


def test_registration_success():
    email = f"register_{uuid4().hex}@example.com"

    response = client.post(
        "/auth/register",
        json={
            "name": "Registration Test",
            "email": email,
            "password": "TestPassword123!",
        },
    )

    try:
        assert response.status_code == 200, response.text

        result = response.json()
        assert result["message"] == "User registered successfully"
        assert result["email"] == email
        assert result["role"] == "user"

    finally:
        # Remove the temporary registered account.
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user:
                db.delete(user)
                db.commit()
        finally:
            db.close()


def test_registration_rejects_duplicate_email(test_user):
    response = client.post(
        "/auth/register",
        json={
            "name": "Duplicate Test",
            "email": test_user["email"],
            "password": "AnotherPassword123!",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_rejects_wrong_password(test_user):
    response = client.post(
        "/auth/login",
        data={
            "username": test_user["email"],
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401


def test_me_requires_authentication():
    response = client.get("/auth/me")

    assert response.status_code in (401, 403)


def test_me_returns_authenticated_user(test_user):
    # Create a real password hash so the login endpoint can verify it.
    from routes.auth import pwd_context

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == test_user["email"]
        ).first()

        user.password = pwd_context.hash(test_user["password"])
        db.commit()
    finally:
        db.close()

    token = get_auth_token(
        test_user["email"],
        test_user["password"],
    )

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text
    assert response.json()["email"] == test_user["email"]
    assert response.json()["role"] == "user"


def test_analytics_with_authenticated_user(test_user):
    from routes.auth import pwd_context

    db = SessionLocal()

    try:
        user = db.query(User).filter(
            User.email == test_user["email"]
        ).first()

        user.password = pwd_context.hash(test_user["password"])
        db.commit()
    finally:
        db.close()

    token = get_auth_token(
        test_user["email"],
        test_user["password"],
    )

    response = client.get(
        "/user/analytics/dashboard",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200, response.text

    result = response.json()

    assert "latest_skin_score" in result
    assert "trend" in result
    assert "progress_entries" in result

def test_progress_log_create_and_list(test_user):
    token = get_auth_token(
        test_user["email"],
        test_user["password"]
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    progress_id = None

    try:
        # 1. Create a skin progress entry
        progress_data = {
            "log_date": "2026-10-18",
            "skin_score": 78,
            "routine_adherence": 85,
            "acne_level": "low",
            "dryness_level": "moderate",
            "pigmentation_level": "low",
            "sensitivity_level": "low",
            "notes": "Progress tracking API test"
        }

        post_response = client.post(
            "/user/progress",
            json=progress_data,
            headers=headers
        )

        assert post_response.status_code == 200, post_response.text

        created_progress = post_response.json()
        progress_id = created_progress["id"]

        assert created_progress["skin_score"] == 78
        assert created_progress["routine_adherence"] == 85
        assert created_progress["user_id"] == test_user["id"]

        # 2. Retrieve the user's progress entries
        get_response = client.get(
            "/user/progress",
            headers=headers
        )

        assert get_response.status_code == 200, get_response.text

        progress_entries = get_response.json()

        # Confirm the newly created entry is returned
        assert any(
            entry["id"] == progress_id
            for entry in progress_entries
        )

    finally:
        # 3. Delete the test entry so it doesn't remain in the database
        if progress_id is not None:
            client.delete(
                f"/user/progress/{progress_id}",
                headers=headers
            )

def test_users_can_only_access_their_own_progress(test_user):
    from uuid import uuid4

    # Create a second, independent user
    second_email = f"second_{uuid4().hex}@example.com"
    second_password = "SecondPassword123!"

    db = SessionLocal()
    try:
        from routes.auth import pwd_context

        second_user = User(
            name="Second Test User",
            email=second_email,
            password=pwd_context.hash(second_password),
            role="user"
        )
        db.add(second_user)
        db.commit()
    finally:
        db.close()

    token_a = get_auth_token(
        test_user["email"],
        test_user["password"]
    )
    token_b = get_auth_token(
        second_email,
        second_password
    )

    headers_a = {"Authorization": f"Bearer {token_a}"}
    headers_b = {"Authorization": f"Bearer {token_b}"}

    progress_id = None

    try:
        # User A creates a progress entry
        response_a = client.post(
            "/user/progress",
            json={
                "log_date": "2026-10-18",
                "skin_score": 82,
                "routine_adherence": 90,
                "notes": "Private test entry"
            },
            headers=headers_a
        )

        assert response_a.status_code == 200, response_a.text
        progress_id = response_a.json()["id"]

        # User B lists their own progress
        response_b = client.get(
            "/user/progress",
            headers=headers_b
        )

        assert response_b.status_code == 200, response_b.text
        assert all(
            entry["id"] != progress_id
            for entry in response_b.json()
        )

    finally:
        # Remove the progress entry created by User A
        if progress_id is not None:
            client.delete(
                f"/user/progress/{progress_id}",
                headers=headers_a
            )

        # Remove the second test user
        cleanup_db = SessionLocal()
        try:
            saved_user = (
                cleanup_db.query(User)
                .filter(User.email == second_email)
                .first()
            )
            if saved_user:
                cleanup_db.delete(saved_user)
                cleanup_db.commit()
        finally:
            cleanup_db.close()

def test_analytics_reflects_saved_progress(test_user):
    token = get_auth_token(
        test_user["email"],
        test_user["password"]
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    progress_id = None

    try:
        # Step 1: Save a skin progress entry
        progress_response = client.post(
            "/user/progress",
            json={
                "log_date": "2026-10-18",
                "skin_score": 75,
                "routine_adherence": 80,
                "notes": "Analytics integration test"
            },
            headers=headers
        )

        assert progress_response.status_code == 200, (
            progress_response.text
        )

        progress_id = progress_response.json()["id"]

        # Step 2: Request the analytics dashboard
        analytics_response = client.get(
            "/user/analytics/dashboard",
            headers=headers
        )

        assert analytics_response.status_code == 200, (
            analytics_response.text
        )

        analytics = analytics_response.json()

        # Step 3: Verify that analytics include the saved progress
        assert analytics["latest_skin_score"] == 75
        assert analytics["latest_routine_adherence"] == 80
        assert analytics["progress_entries"] >= 1

        assert any(
            item["skin_score"] == 75
            for item in analytics["progress_timeline"]
        )

    finally:
        # Clean up the test record
        if progress_id is not None:
            client.delete(
                f"/user/progress/{progress_id}",
                headers=headers
            )

def test_progress_rejects_invalid_skin_score(test_user):
    token = get_auth_token(
        test_user["email"],
        test_user["password"]
    )

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post(
        "/user/progress",
        json={
            "log_date": "2026-10-19",
            "skin_score": 150,
            "routine_adherence": 80,
            "notes": "Invalid score test"
        },
        headers=headers
    )

    assert response.status_code == 422, response.text

def test_progress_creation_requires_authentication():
    response = client.post(
        "/user/progress",
        json={
            "log_date": "2026-10-19",
            "skin_score": 75,
            "routine_adherence": 80,
            "notes": "Unauthenticated test"
        }
    )

    assert response.status_code in (401, 403), response.text
