import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "Dockerfile"
DOCKERIGNORE = ROOT / ".dockerignore"


def dockerfile_instructions() -> list[str]:
    return [
        line.strip()
        for line in DOCKERFILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def find_instruction(name: str) -> list[tuple[int, str]]:
    prefix = name.upper() + " "
    return [
        (index, line)
        for index, line in enumerate(dockerfile_instructions())
        if line.upper().startswith(prefix)
    ]


def test_uses_python_312_slim_base_image() -> None:
    from_lines = find_instruction("FROM")

    assert from_lines, "FROM 명령으로 베이스 이미지를 지정하세요."
    image = from_lines[0][1].split()[1].lower()
    assert image == "python:3.12-slim", "python:3.12-slim 이미지를 사용하세요."


def test_sets_app_working_directory() -> None:
    assert any(
        line.split(maxsplit=1)[1] == "/app" for _, line in find_instruction("WORKDIR")
    ), "WORKDIR를 /app으로 지정하세요."


def test_installs_dependencies_before_copying_application() -> None:
    instructions = dockerfile_instructions()
    requirements_copy = next(
        (
            index
            for index, line in enumerate(instructions)
            if line.upper().startswith(("COPY ", "ADD "))
            and "requirements.txt" in line
        ),
        None,
    )
    app_copy = next(
        (
            index
            for index, line in enumerate(instructions)
            if line.upper().startswith(("COPY ", "ADD "))
            and re.search(r"(^|\s)(\./)?app/?(\s|$)", line, re.IGNORECASE)
        ),
        None,
    )
    pip_install = next(
        (
            index
            for index, line in enumerate(instructions)
            if line.upper().startswith("RUN ")
            and re.search(r"\bpip(?:3)?\s+install\b", line, re.IGNORECASE)
            and "requirements.txt" in line
            and "--no-cache-dir" in line
        ),
        None,
    )

    assert requirements_copy is not None, "requirements.txt를 먼저 COPY하세요."
    assert pip_install is not None, "--no-cache-dir로 requirements.txt를 설치하세요."
    assert app_copy is not None, "app 디렉터리를 이미지에 COPY하세요."
    app_destination = instructions[app_copy].split()[-1].rstrip("/")
    assert app_destination in {"app", "./app", "/app/app"}, (
        "app 디렉터리를 /app/app에 COPY하세요."
    )
    assert requirements_copy < pip_install < app_copy, (
        "의존성 복사 → 설치 → app 복사 순서로 레이어를 구성하세요."
    )


def test_creates_and_uses_non_root_user() -> None:
    run_lines = [line for _, line in find_instruction("RUN")]
    users = find_instruction("USER")

    assert any(
        re.search(r"\b(useradd|adduser)\b", line, re.IGNORECASE) for line in run_lines
    ), "RUN 명령에서 일반 사용자를 생성하세요."
    assert users, "USER 명령으로 실행 사용자를 전환하세요."
    selected_user = users[-1][1].split(maxsplit=1)[1].strip().lower()
    assert selected_user not in {"0", "root"}, "컨테이너를 root로 실행하면 안 됩니다."


def test_exposes_port_8000() -> None:
    exposed = [line.split()[1:] for _, line in find_instruction("EXPOSE")]

    assert any(
        port.split("/")[0] == "8000" for ports in exposed for port in ports
    ), "EXPOSE로 8000 포트를 문서화하세요."


def test_cmd_runs_uvicorn_in_exec_form() -> None:
    commands = find_instruction("CMD")

    assert commands, "CMD를 작성하세요."
    raw_value = commands[-1][1].split(maxsplit=1)[1]
    try:
        command = json.loads(raw_value)
    except json.JSONDecodeError as error:
        raise AssertionError("CMD는 JSON 배열인 exec 형식으로 작성하세요.") from error

    assert isinstance(command, list), "CMD는 JSON 배열이어야 합니다."
    assert command == [
        "uvicorn",
        "app.main:app",
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
    ], "README에 지정된 uvicorn 명령을 exec 형식으로 실행하세요."


def test_dockerignore_excludes_unneeded_files() -> None:
    patterns = {
        line.strip().rstrip("/")
        for line in DOCKERIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }

    required_groups = {
        ".git": {".git", "**/.git"},
        ".venv": {".venv", "**/.venv"},
        "__pycache__": {"__pycache__", "**/__pycache__"},
        "*.pyc": {"*.pyc", "**/*.pyc"},
        ".pytest_cache": {".pytest_cache", "**/.pytest_cache"},
        "tests": {"tests", "**/tests"},
        ".env": {".env", "**/.env"},
        ".env.*": {".env.*", "**/.env.*"},
    }
    missing = [
        label
        for label, accepted in required_groups.items()
        if patterns.isdisjoint(accepted)
    ]

    assert not missing, f".dockerignore에 다음 항목을 추가하세요: {', '.join(missing)}"
