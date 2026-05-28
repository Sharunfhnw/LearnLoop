import bcrypt
from sqlmodel import select
from domain.models import User


class AuthService:
    """Business logic for authentication.

    Responsible for:
    - Password hashing with bcrypt
    - Login validation
    - New user registration
    - Password changes
    """

    def hash_password(self, password: str) -> str:
        """Hash a plain text password with bcrypt and return a string hash."""
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, password: str, stored_hash: str) -> bool:
        """Verify a plain text password against a stored bcrypt hash."""
        if not password or not stored_hash:
            return False
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8")
            )
        except ValueError:
            return False

    def login(self, session, username: str, password: str):
        """Return the user if username exists and password is correct."""
        user = session.exec(
            select(User).where(User.username == username)
        ).first()

        if user and self.check_password(password, user.password_hash):
            return user
        return None

    def register(
        self,
        session,
        username: str,
        email: str,
        password: str,
        role: str
    ) -> User:
        """Create a new user and save it in the database."""
        user = User(
            username=username,
            email=email,
            password_hash=self.hash_password(password),
            role=role
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    def change_password(
        self,
        session,
        user: User,
        old_password: str,
        new_password: str
    ) -> bool:
        """Change password after validating the old password."""
        if not user or not self.check_password(old_password, user.password_hash):
            return False

        user.password_hash = self.hash_password(new_password)
        session.add(user)
        session.commit()
        return True
