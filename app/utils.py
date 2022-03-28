"""
Utils for hashing and verifiyng password
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    """Hash password and return hash"""
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify if hashed given password equals the stored hashed password"""
    return pwd_context.verify(plain_password, hashed_password)
