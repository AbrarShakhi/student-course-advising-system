def serialize_student(student):
    return {
        "student_id": student.student_id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "email": student.email,
        "mobile_no": student.mobile_no,
        "address": student.address,
        "gardian_name": student.gardian_name,
        "gardian_phone": student.gardian_phone,
        "is_dismissed": student.is_dismissed,
        "is_graduated": student.is_graduated,
        "credit_completed": float(student.credit_completed),
        "dept_id": student.dept_id,
        # Add more fields as needed
    }
