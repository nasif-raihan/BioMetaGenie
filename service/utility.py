import logging
import subprocess
import time
from pathlib import Path


def time_execution(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()
        result = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        elapsed_time_ns = end_time - start_time

        hours, remainder = divmod(elapsed_time_ns, 3600 * 10**9)
        minutes, remainder = divmod(remainder, 60 * 10**9)
        seconds, nanoseconds = divmod(remainder, 10**9)

        formatted_time = f"{int(hours):0d}h {int(minutes):02d}m {int(seconds):02d}s {int(nanoseconds):09d}ns"
        print(f"Execution time (function -> {func.__name__}): {formatted_time}")
        return result

    return wrapper


def setup_logger(
    name: str,
    log_directory: Path = Path("../logs"),
    has_file_handler: bool = True,
    has_console_handler: bool = False,
):
    log_directory.mkdir(exist_ok=True)
    log_filepath = log_directory / f"{name}.log"
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        fmt="%(asctime)s - [%(levelname)s] - %(filename)s.%(funcName)s[%(lineno)d]: %(message)s"
    )

    if has_file_handler:
        file_handler = logging.FileHandler(filename=log_filepath, mode="a")
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

    if has_console_handler:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)
        logger.addHandler(console_handler)

    return logger


def run_command(
    command: list[str], logger: logging.Logger = logging.getLogger(__name__)
):
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.cmd}\nOutput: {e.output}\nError: {e.stderr}")
        return False
