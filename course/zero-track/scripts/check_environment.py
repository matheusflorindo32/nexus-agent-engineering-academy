"""Safe local environment checker for NEXUS Zero Track Z00."""
from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def command_version(command: str, args: list[str]) -> dict[str, Any]:
    executable = shutil.which(command)
    if executable is None:
        return {"available": False, "version": None}
    try:
        completed = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": True, "version": None, "error": type(exc).__name__}

    output = (completed.stdout or completed.stderr).strip().splitlines()
    return {
        "available": True,
        "version": output[0] if output else "unknown",
        "exit_code": completed.returncode,
    }


def build_report() -> dict[str, Any]:
    return {
        "schema": "nexus.zero-track.environment.v1",
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        },
        "working_directory_name": Path.cwd().name,
        "tools": {
            "git": command_version("git", ["--version"]),
            "python": command_version(sys.executable, ["--version"]),
        },
        "privacy_note": (
            "The report intentionally omits usernames, home paths, environment "
            "variables, network addresses and file contents."
        ),
    }


def main() -> None:
    print(json.dumps(build_report(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
