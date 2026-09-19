from fastapi import FastAPI, HTTPException, status

from app.repository import StudyRecordRepository
from app.schemas import StudyRecordCreate, StudyRecordResponse

app = FastAPI(title="Study Record API")
repository = StudyRecordRepository()


@app.get("/health")
def health() -> dict[str, str]:
    return { "status": "ok" }


@app.post(
    "/api/v1/study-records",
    response_model=StudyRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_study_record(data: StudyRecordCreate) -> StudyRecordResponse:
    record = repository.create(data)
    return record


@app.get("/api/v1/study-records", response_model=list[StudyRecordResponse])
def list_study_records() -> list[StudyRecordResponse]:
    records = repository.list_all()
    return records


@app.get(
    "/api/v1/study-records/{record_id}", response_model=StudyRecordResponse
)
def get_study_record(record_id: int) -> StudyRecordResponse:
    record = repository.get(record_id=record_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study record not found"
        )

    return record


@app.patch(
    "/api/v1/study-records/{record_id}/complete",
    response_model=StudyRecordResponse,
)
def complete_study_record(record_id: int) -> StudyRecordResponse:
    record = repository.complete(record_id=record_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Study record not found"
        )

    return record

    
