from .validator import validate_persons, validate_salaries
from .abstract_person_validations.phone_validator import is_valid_phone_number

__all__ = (validate_persons, is_valid_phone_number, validate_salaries)
