class StudyNoteNotFoundError(Exception):
    def __init__(self) -> None:
        super().__init__("Study note not found")

