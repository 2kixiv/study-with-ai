from app.schemas import StudyRecordCreate, StudyRecordResponse


class StudyRecordRepository:
    """학습 기록을 메모리에 저장합니다."""

    def __init__(self) -> None:
        self._records: dict[int, StudyRecordResponse] = {}
        self._next_id = 1

    def create(self, data: StudyRecordCreate) -> StudyRecordResponse:
        _id = self.next_id()

        record = StudyRecordResponse(
            id=_id,
            topic=data.topic,
            minutes=data.minutes,
            completed=False,
        )

        self._records.update({ _id : record })

        return record

    def list_all(self) -> list[StudyRecordResponse]:
        return list(self._records.values())

    def get(self, record_id: int) -> StudyRecordResponse | None:
        return self._records.get(record_id)

    def complete(self, record_id: int) -> StudyRecordResponse | None:
        record = self._records.get(record_id)

        if record is None:
            return None

        record.completed = True

        return record

    def next_id(self) -> int:
        tmp = self._next_id
        self._next_id += 1
        return tmp

    def clear(self) -> None:
        """테스트마다 독립된 상태를 사용하기 위한 초기화 메서드입니다."""
        self._records.clear()
        self._next_id = 1