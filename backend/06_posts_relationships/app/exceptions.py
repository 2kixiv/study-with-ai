class DuplicateEmailError(Exception):
    def __init__(self) -> None: super().__init__("Email already exists")
class InvalidCredentialsError(Exception):
    def __init__(self) -> None: super().__init__("Invalid credentials")
class InactiveUserError(Exception):
    def __init__(self) -> None: super().__init__("Inactive user")
class PostNotFoundError(Exception):
    def __init__(self) -> None: super().__init__("Post not found")
class NotPostOwnerError(Exception):
    def __init__(self) -> None: super().__init__("Not post owner")

