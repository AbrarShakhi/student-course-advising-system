from django.contrib.auth.hashers import check_password, make_password


def hash_password(raw_password):
    return make_password(raw_password)


def compare_password(raw_password, hashed_password):
    return check_password(raw_password, hashed_password)
