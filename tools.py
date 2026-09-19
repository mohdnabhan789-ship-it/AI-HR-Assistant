from app.database import employees


def check_leave_balance(employee_id: str):
    """Check how many leave days an employee has remaining."""

    employee = employees.get(employee_id)

    if employee is None:
        return "Employee not found."

    leave = employee["leave_balance"]

    return f"You have {leave} leave days remaining."


def check_attendance(employee_id: str):
    """Check an employee's attendance percentage."""

    employee = employees.get(employee_id)

    if employee is None:
        return "Employee not found."

    attendance = employee["attendance"]

    return f"Your attendance percentage is {attendance}%."


def get_employee_details(employee_id: str):
    """Get an employee's name, department, and role."""

    employee = employees.get(employee_id)

    if employee is None:
        return "Employee not found."

    return (
        f"Name: {employee['name']}\n"
        f"Department: {employee['department']}\n"
        f"Role: {employee['role']}"
    )