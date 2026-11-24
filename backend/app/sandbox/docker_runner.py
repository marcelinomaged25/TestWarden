"""Run generated tests inside a locked-down Docker container."""

SANDBOX_FLAGS = ["--network", "none", "--memory", "512m", "--user", "1000:1000"]
TIMEOUT_SECONDS = 60


def run_in_sandbox(repo_path: str, test_file: str) -> dict:
    raise NotImplementedError("Week 2: first Docker sandbox")
