import re
import subprocess
from pathlib import Path
from typing import Set

from service.utility import setup_logger


class TrimGaloreTrimmer:
    def __init__(self):
        self.trim_galore_path = Path("./third_party/TrimGalore/trim_galore")
        self.raw_seq_directory = Path("./output/fastq_files")
        self.output_directory = Path("./output/trimmed_fastq_files")
        self.sample_stats_dir = Path("./output/sample_stats")
        self.fq_word_count_path = Path("./output/fq_word_count.txt")

        self.logger = setup_logger(name="trim_galore", has_console_handler=True)

    def trim(self):
        unique_prefixes = self.get_unique_prefixes
        total_kit_count = len(unique_prefixes)
        for index, kit_id in enumerate(unique_prefixes):
            self.run_trim_galore(kit_id)
            self.logger.info(
                f"#--- Completed trimming of {index+1}/{total_kit_count} ---#"
            )
        self.get_sample_stats()

    def get_sample_stats(self):
        self.sample_stats_dir.mkdir(parents=True, exist_ok=True)
        sample_stats_path = self.sample_stats_dir / "sample_stats.txt"
        fq_files = list(self.output_directory.glob("*.fq"))

        with sample_stats_path.open("w") as stats_file:
            subprocess.run(
                ["seqkit", "stats"] + [str(fq_file) for fq_file in fq_files],
                stdout=stats_file,
            )

        self.logger.info(
            f"Generated seqkit statistics of sequences at {str(sample_stats_path)}"
        )

    @property
    def get_unique_prefixes(self) -> Set[str]:
        return {
            re.split(r"[-_]", file.stem)[0]
            for file in self.raw_seq_directory.glob("*.fastq")
        }

    def run_trim_galore(self, kit_id: str):
        self.output_directory.mkdir(parents=True, exist_ok=True)
        input_files = [self.raw_seq_directory / f"{kit_id}_{i}.fastq" for i in (1, 2)]
        command = [
            str(self.trim_galore_path),
            "--paired",
            "--quality",
            "30",
            "--length",
            "50",
            *map(str, input_files),
            "--fastqc",
            "--output_dir",
            str(self.output_directory),
        ]

        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            self.logger.info(f"Trimming completed successfully for kit: {kit_id}")
        except subprocess.CalledProcessError as e:
            self.logger.error(
                f"Command failed for kit: {kit_id}\nError: {e.stderr.strip()}"
            )
