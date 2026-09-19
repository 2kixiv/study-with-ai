class UserNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("User not found")


class DuplicateEmailError(Exception):
    def __init__(self) -> None:
        super().__init__("Email already exists")

