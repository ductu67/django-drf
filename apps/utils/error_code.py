from enum import Enum


class ErrorCode(Enum):
    unknown_error = "Unknown Error"
    wrong_email_pass = "Invalid email or password. Please try again!"
    invalid_token = "Invalid token"
    invalid_credential = "Invalid token header. No credentials provided."
    invalid_format_token = "Invalid token header. Token string should not contain spaces."
    invalid_character_token = "Invalid token header. Token string should not contain invalid characters."
    token_expired = "Token Expired!"
    exception_token = "Invalid token and expired."
    token_empty = "Invalid Token! please Logout and Relogin"
    not_found_token = "No user matching this token was found."
    validate_month = "can't change the previous month"
    number_project = "A staff can't join more than 3 projects"
    validate_effort = "effort must be less than 1 and more than 0"
    validate_plan_effort = "Plan Effort must be greater than 0"
    validate_date = "Start date must be less than end_date"
