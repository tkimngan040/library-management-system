"""
Shared Validation Functions
Used by all team members for consistent input validation
"""

import re
from typing import Tuple


class Validators:
    """Shared validation functions for the Library Management System"""
    
    # ==================== STRING VALIDATIONS ====================
    
    @staticmethod
    def validate_not_empty(value: str, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate that a string is not empty
        
        Args:
            value: String to validate
            field_name: Name of the field for error message
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not value or not value.strip():
            return False, f"{field_name} cannot be empty!"
        return True, ""
    
    @staticmethod
    def validate_string_length(value: str, min_length: int = 1, 
                              max_length: int = 255, 
                              field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate string length
        
        Args:
            value: String to validate
            min_length: Minimum length
            max_length: Maximum length
            field_name: Name of the field
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if len(value) < min_length:
            return False, f"{field_name} must be at least {min_length} characters!"
        
        if len(value) > max_length:
            return False, f"{field_name} cannot exceed {max_length} characters!"
        
        return True, ""
    
    @staticmethod
    def validate_alpha_only(value: str, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate that string contains only letters and spaces
        
        Args:
            value: String to validate
            field_name: Name of the field
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not re.match(r'^[a-zA-Z\s]+$', value):
            return False, f"{field_name} can only contain letters and spaces!"
        return True, ""
    
    @staticmethod
    def validate_alphanumeric(value: str, field_name: str = "Field") -> Tuple[bool, str]:
        """
        Validate that string contains only letters, numbers, and spaces
        
        Args:
            value: String to validate
            field_name: Name of the field
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not re.match(r'^[a-zA-Z0-9\s]+$', value):
            return False, f"{field_name} can only contain letters, numbers, and spaces!"
        return True, ""
    
    # ==================== NUMBER VALIDATIONS ====================
    
    @staticmethod
    def validate_positive_integer(value: int, field_name: str = "Value") -> Tuple[bool, str]:
        """
        Validate that value is a positive integer
        
        Args:
            value: Integer to validate
            field_name: Name of the field
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not isinstance(value, int):
            return False, f"{field_name} must be an integer!"
        
        if value <= 0:
            return False, f"{field_name} must be greater than 0!"
        
        return True, ""
    
    @staticmethod
    def validate_non_negative_integer(value: int, field_name: str = "Value") -> Tuple[bool, str]:
        """
        Validate that value is a non-negative integer (>= 0)
        
        Args:
            value: Integer to validate
            field_name: Name of the field
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if not isinstance(value, int):
            return False, f"{field_name} must be an integer!"
        
        if value < 0:
            return False, f"{field_name} cannot be negative!"
        
        return True, ""
    
    @staticmethod
    def validate_number_range(value: int, min_val: int, max_val: int, 
                             field_name: str = "Value") -> Tuple[bool, str]:
        """
        Validate that number is within a range
        
        Args:
            value: Number to validate
            min_val: Minimum value (inclusive)
            max_val: Maximum value (inclusive)
            field_name: Name of the field
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if value < min_val or value > max_val:
            return False, f"{field_name} must be between {min_val} and {max_val}!"
        
        return True, ""
    
    # ==================== USERNAME VALIDATIONS ====================
    
    @staticmethod
    def validate_username(username: str) -> Tuple[bool, str]:
        """
        Validate username format
        Rules:
        - 3-50 characters
        - Only letters, numbers, underscore, hyphen
        - Must start with a letter
        
        Args:
            username: Username to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Check not empty
        is_valid, msg = Validators.validate_not_empty(username, "Username")
        if not is_valid:
            return False, msg
        
        # Check length
        if len(username) < 3:
            return False, "Username must be at least 3 characters!"
        
        if len(username) > 50:
            return False, "Username cannot exceed 50 characters!"
        
        # Check format
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_-]*$', username):
            return False, "Username must start with a letter and contain only letters, numbers, underscore, or hyphen!"
        
        return True, ""
    
    # ==================== PASSWORD VALIDATIONS ====================
    
    @staticmethod
    def validate_password(password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        Rules:
        - At least 6 characters
        - Maximum 100 characters
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Check not empty
        if not password:
            return False, "Password cannot be empty!"
        
        # Check minimum length
        if len(password) < 6:
            return False, "Password must be at least 6 characters!"
        
        # Check maximum length
        if len(password) > 100:
            return False, "Password cannot exceed 100 characters!"
        
        return True, ""
    
    @staticmethod
    def validate_password_strong(password: str) -> Tuple[bool, str]:
        """
        Validate strong password
        Rules:
        - At least 8 characters
        - Contains uppercase letter
        - Contains lowercase letter
        - Contains number
        - Contains special character
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters!"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter!"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter!"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one number!"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character!"
        
        return True, ""
    
    # ==================== EMAIL VALIDATIONS ====================
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email format
        
        Args:
            email: Email to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Allow empty email (optional field)
        if not email or not email.strip():
            return True, ""
        
        # Check email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format!"
        
        # Check length
        if len(email) > 255:
            return False, "Email cannot exceed 255 characters!"
        
        return True, ""
    
    # ==================== PHONE VALIDATIONS ====================
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """
        Validate phone number
        Accepts: Vietnamese phone formats (10-11 digits)
        
        Args:
            phone: Phone number to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Allow empty phone (optional field)
        if not phone or not phone.strip():
            return True, ""
        
        # Remove spaces and hyphens
        phone_clean = phone.replace(' ', '').replace('-', '')
        
        # Check if only digits
        if not phone_clean.isdigit():
            return False, "Phone number can only contain digits!"
        
        # Check length (Vietnamese phone: 10-11 digits)
        if len(phone_clean) < 10 or len(phone_clean) > 11:
            return False, "Phone number must be 10-11 digits!"
        
        return True, ""
    
    # ==================== DATE VALIDATIONS ====================
    
    @staticmethod
    def validate_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> Tuple[bool, str]:
        """
        Validate date string format
        
        Args:
            date_str: Date string to validate
            format_str: Expected date format (default: YYYY-MM-DD)
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        from datetime import datetime
        
        try:
            datetime.strptime(date_str, format_str)
            return True, ""
        except ValueError:
            return False, f"Invalid date format! Expected format: {format_str}"
    
    # ==================== BOOK VALIDATIONS ====================
    
    @staticmethod
    def validate_book_title(title: str) -> Tuple[bool, str]:
        """
        Validate book title
        
        Args:
            title: Book title to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Check not empty
        is_valid, msg = Validators.validate_not_empty(title, "Book title")
        if not is_valid:
            return False, msg
        
        # Check length
        is_valid, msg = Validators.validate_string_length(
            title, min_length=1, max_length=255, field_name="Book title"
        )
        if not is_valid:
            return False, msg
        
        return True, ""
    
    @staticmethod
    def validate_author_name(author: str) -> Tuple[bool, str]:
        """
        Validate author name
        
        Args:
            author: Author name to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Check not empty
        is_valid, msg = Validators.validate_not_empty(author, "Author name")
        if not is_valid:
            return False, msg
        
        # Check length
        is_valid, msg = Validators.validate_string_length(
            author, min_length=1, max_length=100, field_name="Author name"
        )
        if not is_valid:
            return False, msg
        
        return True, ""
    
    @staticmethod
    def validate_category(category: str) -> Tuple[bool, str]:
        """
        Validate book category
        
        Args:
            category: Category to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        # Check not empty
        is_valid, msg = Validators.validate_not_empty(category, "Category")
        if not is_valid:
            return False, msg
        
        # Check length
        is_valid, msg = Validators.validate_string_length(
            category, min_length=1, max_length=50, field_name="Category"
        )
        if not is_valid:
            return False, msg
        
        return True, ""
    
    @staticmethod
    def validate_book_quantity(quantity: int) -> Tuple[bool, str]:
        """
        Validate book quantity
        
        Args:
            quantity: Quantity to validate
            
        Returns:
            Tuple of (is_valid: bool, message: str)
        """
        return Validators.validate_positive_integer(quantity, "Quantity")
    
    # ==================== UTILITY FUNCTIONS ====================
    
    @staticmethod
    def sanitize_input(value: str) -> str:
        """
        Sanitize user input by stripping whitespace
        
        Args:
            value: Input string
            
        Returns:
            Sanitized string
        """
        if not value:
            return ""
        return value.strip()
    
    @staticmethod
    def validate_all(validations: list) -> Tuple[bool, str]:
        """
        Run multiple validations and return first error
        
        Args:
            validations: List of (is_valid, message) tuples
            
        Returns:
            Tuple of (all_valid: bool, first_error_message: str)
        """
        for is_valid, message in validations:
            if not is_valid:
                return False, message
        return True, ""


# Convenience functions for quick validation
def is_valid_username(username: str) -> bool:
    """Quick check if username is valid"""
    is_valid, _ = Validators.validate_username(username)
    return is_valid


def is_valid_email(email: str) -> bool:
    """Quick check if email is valid"""
    is_valid, _ = Validators.validate_email(email)
    return is_valid


def is_valid_phone(phone: str) -> bool:
    """Quick check if phone is valid"""
    is_valid, _ = Validators.validate_phone(phone)
    return is_valid


def is_valid_password(password: str) -> bool:
    """Quick check if password is valid"""
    is_valid, _ = Validators.validate_password(password)
    return is_valid
