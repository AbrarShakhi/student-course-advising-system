import requests

BASE_URL = "http://localhost:5000/api"

# Session object to persist cookies (JWT) automatically across requests
session = requests.Session()


def test_login(student_id, password):
    url = f"{BASE_URL}/login"
    payload = {"student_id": student_id, "password": password}
    response = session.post(url, json=payload)
    print("Login Response:", response.status_code, response.text)
    return response


def test_logout():
    url = f"{BASE_URL}/logout"
    response = session.get(url)
    print("Logout Response:", response.status_code, response.text)
    return response


def test_activate(student_id, password, otp):
    url = f"{BASE_URL}/activate"
    payload = {"student_id": student_id, "password": password, "otp": otp}
    response = session.post(url, json=payload)
    print("Activate Response:", response.status_code, response.text)
    return response


def test_forgot_password(student_id, password, otp):
    url = f"{BASE_URL}/forgot-password"
    payload = {"student_id": student_id, "password": password, "otp": otp}
    response = session.post(url, json=payload)
    print("Forgot Password Response:", response.status_code, response.text)
    return response


def test_send_otp(student_id, reason_id):
    url = f"{BASE_URL}/send-otp"
    params = {"reason_id": reason_id}
    payload = {"student_id": student_id}
    response = session.patch(url, params=params, json=payload)
    print("Send OTP Response:", response.status_code, response.text)
    return response


def test_welcome():
    url = f"{BASE_URL}/welcome"
    response = session.get(url)
    print("Welcome Response:", response.status_code, response.text)
    return response


def test_change_password(old_password, new_password):
    url = f"{BASE_URL}/change-password"
    payload = {"old_password": old_password, "new_password": new_password}
    response = session.patch(url, json=payload)
    print("Change Password Response:", response.status_code, response.text)
    return response


def test_list_semesters():
    url = f"{BASE_URL}/list-semesters"
    response = session.get(url)
    print("List Semesters Response:", response.status_code, response.text)
    return response


def test_university_info():
    url = f"{BASE_URL}/university-info"
    response = session.get(url)
    print("University Info Response:", response.status_code, response.text)
    return response


def test_class_schedule(season_id=None, year=None):
    url = f"{BASE_URL}/class-schedule"
    params = {}
    if season_id:
        params["season_id"] = season_id
    if year:
        params["year"] = year
    response = session.get(url, params=params)
    print("Class Schedule Response:", response.status_code, response.text)
    return response


if __name__ == "__main__":
    # Replace these sample values with valid test data
    student_id = "2022-3-60-022"
    password = "123456789"
    new_password = "1234567890"
    otp = "123456"
    old_password = password
    reason_id_activation = "2"  # for activate
    reason_id_password = "1"  # for password reset

    print("Testing /login...")
    test_login(student_id, password)

    # print("\nTesting /welcome (requires JWT)...")
    # test_welcome()

    # print("\nTesting /send-otp for activation...")
    # test_send_otp(student_id, reason_id_activation)

    # print("\nTesting /activate...")
    # test_activate(student_id, new_password, otp)

    # print("\nTesting /send-otp for password reset...")
    # test_send_otp(student_id, reason_id_password)

    # print("\nTesting /forgot-password...")
    # test_forgot_password(student_id, new_password, otp)

    # print("\nTesting /change-password...")
    # test_change_password(old_password, new_password)

    # print("\nTesting /list-semesters...")
    # test_list_semesters()

    # print("\nTesting /university-info...")
    # test_university_info()

    print("\nTesting /class-schedule...")
    test_class_schedule(season_id=1, year=2024)

    print("\nTesting /logout...")
    test_logout()
