
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    import re
    pattern = r'^[0-9]{10,11}$'
    return re.match(pattern, phone) is not None

def validate_password(password):
    return len(password) >= 6
