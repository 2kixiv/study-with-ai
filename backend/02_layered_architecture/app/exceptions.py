class StudyTaskNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Study task not found")


class DuplicateActiveTaskError(Exception):
    def __init__(self) -> None:
        super().__init__("Active task with this title already exists")


class StudyTaskAlreadyCompletedError(Exception):
    def __init__(self) -> None:
        super().__init__("Study task is already completed")