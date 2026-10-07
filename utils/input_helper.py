import re


class InputHelper:
    EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

    @staticmethod
    def get_non_empty(prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")

    @staticmethod
    def get_name(prompt):
        while True:
            value = input(prompt).strip()
            if value and all(ch.isalpha() or ch.isspace() or ch in ".-" for ch in value):
                return value
            print("Enter a valid name.")

    @staticmethod
    def get_int(prompt, minimum, maximum):
        while True:
            try:
                value = int(input(prompt).strip())
                if minimum <= value <= maximum:
                    return value
                print(f"Enter a number from {minimum} to {maximum}.")
            except ValueError:
                print("Please enter a valid integer.")

    @staticmethod
    def get_float(prompt, minimum, maximum):
        while True:
            try:
                value = float(input(prompt).strip())
                if minimum <= value <= maximum:
                    return value
                print(f"Enter a number from {minimum} to {maximum}.")
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def get_email(prompt):
        while True:
            value = input(prompt).strip()
            if InputHelper.EMAIL_RE.match(value):
                return value
            print("Enter a valid email address.")

    @staticmethod
    def get_optional_int(prompt, minimum, maximum, default):
        while True:
            value = input(prompt).strip()
            if not value:
                return default
            try:
                value = int(value)
                if minimum <= value <= maximum:
                    return value
                print(f"Enter a number from {minimum} to {maximum}.")
            except ValueError:
                print("Please enter a valid integer.")

    @staticmethod
    def get_optional_float(prompt, minimum, maximum, default):
        while True:
            value = input(prompt).strip()
            if not value:
                return default
            try:
                value = float(value)
                if minimum <= value <= maximum:
                    return value
                print(f"Enter a number from {minimum} to {maximum}.")
            except ValueError:
                print("Please enter a valid number.")

    @staticmethod
    def get_optional_email(prompt, default):
        while True:
            value = input(prompt).strip()
            if not value:
                return default
            if InputHelper.EMAIL_RE.match(value):
                return value
            print("Enter a valid email address.")

    @staticmethod
    def get_choice(prompt, minimum, maximum):
        return InputHelper.get_int(prompt, minimum, maximum)
