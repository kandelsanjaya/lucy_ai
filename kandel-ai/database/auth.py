"""
KANDEL AI - Authentication (case-sensitive, bcrypt + JWT)
Designed by Kandel Sanjaya
"""
import bcrypt
import jwt
import datetime
from database.db import get_conn
from config.settings import settings


def _hash_password(password: str) -> str:
    # NOTE: password is used exactly as typed - no .lower()/.strip() normalization,
    # so authentication is strictly case-sensitive.
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except Exception:
        return False


def signup(name: str, email: str, password: str):
    email_key = email.strip()  # email match is case-insensitive-ish for convenience,
    # but password check below remains fully case-sensitive.
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email = ?", (email_key,))
        if c.fetchone():
            return False, "An account with this email already exists."
        c.execute(
            "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
            (name, email_key, _hash_password(password)),
        )
        return True, "Account created successfully."


def login(email: str, password: str):
    email_key = email.strip()
    with get_conn() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email = ?", (email_key,))
        row = c.fetchone()
        if not row:
            return False, "No account found with this email.", None
        # Case-sensitive check: "Password123" != "password123"
        if not _verify_password(password, row["password_hash"]):
            return False, "Incorrect password (passwords are case-sensitive).", None
        user = dict(row)
        del user["password_hash"]
        return True, "Login successful.", user


def create_token(user: dict) -> str:
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=settings.SESSION_TIMEOUT_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")


def verify_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
