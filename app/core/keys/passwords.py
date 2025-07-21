from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(raw_password) -> str:
    return generate_password_hash(raw_password)


def compare_password(raw_password, hashed_password) -> bool:
    return check_password_hash(hashed_password, raw_password)
