from app.core.database import SessionLocal, init_db
from app.models.user import UserRole
from app.services.user_service import create_user


def main():
    # Ensure tables exist
    init_db()
    db = SessionLocal()
    try:
        # Change these as needed
        name = "Admin"
        email = "admin@example.com"
        password = "admin123"

        user = create_user(db, name=name, email=email, password=password, role=UserRole.ADMIN)
        print(f"Created admin user: {user.email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()

