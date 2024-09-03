import subprocess
from pathlib import Path

from service.utility import time_execution, run_command, setup_logger


class PMBatchAnalyzer:
    def __init__(self):
        self.trimmed_fastq_files = Path("./output/trimmed_fastq_files")
        self.sample_stats_dir = self.trimmed_fastq_files / "sample_stats"
        self.fq_word_count_path = Path("./output/fq_word_count.txt")
        self.usearch_path = Path("./third_party/usearch11.0.667_i86linux32")
        self.pm_path = Path("./third_party/parallel-meta-suite/bin")
        self.output_directory = Path("./output/processed_pm_data")
        self.seqs_list_file = Path("./output/seqs.list")
        self.meta_file = Path("./output/meta.txt")
        self.logger = setup_logger(name="pm_pipeline", has_console_handler=True)

        self.sample_stats_dir.mkdir(parents=True, exist_ok=True)

    def get_sample_stats(self):
        sample_stats_path = self.sample_stats_dir / "sample_stats.txt"
        fq_files = list(self.trimmed_fastq_files.glob("*.fq"))

        with sample_stats_path.open("w") as stats_file:
            subprocess.run(
                ["seqkit", "stats"] + [str(fq_file) for fq_file in fq_files],
                stdout=stats_file,
            )

        # Move sample_stats directory to the parent directory
        parent_dir = self.trimmed_fastq_files.parent
        self.sample_stats_dir.rename(parent_dir / self.sample_stats_dir.name)

    def get_filtered_samples(self) -> list[str]:
        fq_files = list(self.trimmed_fastq_files.glob("*.fq"))

        with self.fq_word_count_path.open("w") as fq_word_count_file:
            for fq_file in fq_files:
                result = subprocess.run(
                    ["wc", "-l", str(fq_file)], capture_output=True, text=True
                )
                fq_word_count_file.write(result.stdout)

        # Remove the last line from fq_word_count.txt
        with self.fq_word_count_path.open("r+") as fq_word_count_file:
            lines = fq_word_count_file.readlines()
            fq_word_count_file.seek(0)
            fq_word_count_file.writelines(lines[:-1])
            fq_word_count_file.truncate()

        sample_seqs_num_dict = {}
        with self.fq_word_count_path.open("r") as file:
            for line in file:
                parts = line.split()
                sample_id = parts[1].split("_")[0]
                num_seqs = int(parts[0]) // 4
                if (
                    sample_seqs_num_dict.get(sample_id)
                    and sample_seqs_num_dict[sample_id] != num_seqs
                ):
                    del sample_seqs_num_dict[sample_id]
                    self.logger.error(
                        f"The read count does not match for sample_id: {sample_id}"
                    )
                else:
                    sample_seqs_num_dict[sample_id] = num_seqs

        filtered_samples = {
            key: value for key, value in sample_seqs_num_dict.items() if value >= 10000
        }

        self.logger.info(f"Trimmed samples count: {list(sample_seqs_num_dict.keys())}")
        self.logger.info(
            f"After filtering samples count: {list(filtered_samples.keys())}"
        )
        return list(filtered_samples.keys())

    @time_execution
    def merge_reads(self, sample_id: str):
        forward_read = self.trimmed_fastq_files / f"{sample_id}_1_val_1.fq"
        reverse_read = self.trimmed_fastq_files / f"{sample_id}_2_val_2.fq"
        merged_file = self.output_directory / f"{sample_id}.merged_file.fq"

        self.output_directory.mkdir(exist_ok=True)

        # fmt: off
        command = [
            str(self.usearch_path), "-fastq_mergepairs", str(forward_read), "-reverse", str(reverse_read), "-relabel",
            "@", "-fastq_maxdiffs", "10", "-fastq_pctid", "80", "-fastqout", str(merged_file),
        ]
        run_command(command)
        # fmt: on

        return merged_file

    @time_execution
    def run_parallel_meta(self):
        self.logger.info("Processing with Parallel Meta started")

        # fmt: off
        pipeline_command = [
            str(self.pm_path / "PM-pipeline"), "-i", str(self.seqs_list_file), "-m", str(self.meta_file), "-o",
            str(self.output_directory),
        ]
        run_command(pipeline_command)

        func_abundance_command = [
            str(self.pm_path / "PM-predict-func"), "-T", str(self.output_directory / "Abundance_Tables/taxa.OTU.Count"),
            "-o", str(self.output_directory / "Abundance_Tables/func"),
        ]
        run_command(func_abundance_command)

        for level in [2, 3]:
            select_func_command = [
                str(self.pm_path / "PM-select-func"), "-T",
                str(self.output_directory / f"Abundance_Tables/func.KO.Count"), "-o",
                str(self.output_directory / "Abundance_Tables/func"), "-L", str(level),
            ]
            run_command(select_func_command)
        # fmt: on

    def analyze(self):
        self.get_sample_stats()
        with self.meta_file.open("w") as meta, self.seqs_list_file.open(
            "w"
        ) as seqs_list:
            meta.write("subject_id\n")

            samples = self.get_filtered_samples()
            for sample_id in samples:
                merged_file = self.merge_reads(sample_id)
                meta.write(f"{sample_id}\n")
                seqs_list.write(f"{sample_id} {merged_file}\n")

        self.run_parallel_meta()
