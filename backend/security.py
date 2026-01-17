import bcrypt


def hash_password(plain_password: str) -> str:
    """
    Hash a plain text password using bcrypt before storing it in the database.
    """
    if not plain_password:
        raise ValueError("Password must not be empty")

    hashed_password = bcrypt.hashpw(
        plain_password.encode("utf-8"),
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.
    """
    if not plain_password or not hashed_password:
        return False

    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )
