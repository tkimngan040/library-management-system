from datetime import date

FINE_PER_DAY = 5000  # 5,000 VND / day


def calculate_fine(due_date, return_date):
    """
    Calculate overdue fine based on due date and actual return date
    """
    if return_date <= due_date:
        return 0, 0

    overdue_days = (return_date - due_date).days
    fine = overdue_days * FINE_PER_DAY
    return overdue_days, fine
