import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock

from service.utility import run_command, time_execution, setup_logger


class NcbiSraDownloader:
    def __init__(self, sra_list_file_path: Path = Path("./input/SRA_list.txt")):
        self.sra_list_file = sra_list_file_path
        self.download_dir = Path("./output/sra_files")
        self.fastq_dir = Path("./output/fastq_files")
        self.download_success_logger = setup_logger("download_success")
        self.download_failure_logger = setup_logger("download_failure")
        self.conversion_success_logger = setup_logger("conversion_success")
        self.conversion_failure_logger = setup_logger("conversion_failure")
        self.stream_logger = setup_logger("stream", has_console_handler=True)

        self.completion_lock = Lock()

    @time_execution
    def process_sra_list(self):
        with open(self.sra_list_file, "r") as file:
            srr_ids = file.read().splitlines()

        total_ids = len(srr_ids)
        completion_counter = {"count": 0}

        with ThreadPoolExecutor(max_workers=10) as executor:
            for srr_id in srr_ids:
                executor.submit(self.process_sra, srr_id, total_ids, completion_counter)

        self.stream_logger.info(
            "#--- All downloads and processing have been completed."
        )

    def process_sra(self, srr_id: str, total_ids: int, completion_counter: dict):
        self.stream_logger.info(f"+------ Started processing for {srr_id} ------+\n")
        if self.download_sra(srr_id):
            self.convert_to_fastq(srr_id)

        with self.completion_lock:
            completion_counter["count"] += 1
            self.stream_logger.info(
                f"+------ Completed processing {completion_counter['count']}/{total_ids} ------+\n"
            )

    def download_sra(self, srr_id: str):
        command = ["prefetch", srr_id, "--output-directory", self.download_dir]
        if run_command(command):
            self.download_success_logger.info(f"Downloaded {srr_id} successfully.")
            return True
        else:
            self.download_failure_logger.error(f"Failed to download {srr_id}.")
            return False

    def convert_to_fastq(self, srr_id: str):
        sra_file = os.path.join(self.download_dir, f"{srr_id}/{srr_id}.sra")
        command_1 = [
            "fastq-dump",
            "--split-files",
            "--outdir",
            self.fastq_dir,
            sra_file,
        ]
        command_2 = ["rm", "-r", f"{self.download_dir}/{srr_id}"]

        if run_command(command_1):
            run_command(command_2)
            self.conversion_success_logger.info(
                f"Converted {srr_id} to FASTQ successfully."
            )
            return True
        else:
            self.conversion_failure_logger.error(
                f"Failed to convert {srr_id} to FASTQ."
            )
            return False
