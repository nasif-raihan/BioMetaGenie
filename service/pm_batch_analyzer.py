import subprocess
from pathlib import Path

from service.utility import time_execution, run_command, setup_logger


class PMBatchAnalyzer:
    def __init__(self):
        self.trimmed_fastq_files = Path("./output/trimmed_fastq_files")
        self.fq_word_count_path = Path("./output/fq_word_count.txt")
        self.usearch_path = Path("./third_party/usearch11.0.667_i86linux32")
        self.pm_path = Path("./third_party/parallel-meta-suite/bin")
        self.pm_output = Path("./output/pm_output")
        self.merged_read = Path("./output/merged_read")
        self.seqs_list_file = Path("./output/seqs.list")
        self.meta_file = Path("./output/meta.txt")
        self.logger = setup_logger(name="pm_pipeline", has_console_handler=True)

    def get_filtered_samples(self) -> list[str]:
        fq_files = list(self.trimmed_fastq_files.glob("*.fq"))

        with self.fq_word_count_path.open("w") as fq_word_count_file:
            for fq_file in fq_files:
                result = subprocess.run(
                    ["wc", "-l", str(fq_file)], capture_output=True, text=True
                )
                fq_word_count_file.write(result.stdout)

        with self.fq_word_count_path.open("r+") as fq_word_count_file:
            lines = fq_word_count_file.readlines()
            fq_word_count_file.seek(0)
            fq_word_count_file.writelines(lines[:-1])
            fq_word_count_file.truncate()

        sample_seqs_num_dict = {}
        with self.fq_word_count_path.open("r") as file:
            for line in file:
                parts = line.split()
                sample_id = parts[1].split("/")[-1].split("_")[0]
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

        self.logger.info(f"Trimmed samples count: {len(sample_seqs_num_dict.keys())}")
        self.logger.info(
            f"After filtering samples count: {len(filtered_samples.keys())}"
        )
        return list(filtered_samples.keys())

    @time_execution
    def merge_reads(self, sample_id: str):
        forward_read = self.trimmed_fastq_files / f"{sample_id}_1_val_1.fq"
        reverse_read = self.trimmed_fastq_files / f"{sample_id}_2_val_2.fq"
        merged_file = self.merged_read / f"{sample_id}.merged_file.fq"

        self.merged_read.mkdir(exist_ok=True)

        # fmt: off
        command = [
            str(self.usearch_path), "-fastq_mergepairs", str(forward_read), "-reverse", str(reverse_read), "-relabel",
            "@", "-fastq_maxdiffs", "10", "-fastq_pctid", "80", "-fastqout", str(merged_file),
        ]
        if run_command(command):
            self.logger.info(f"Successfully merged R1 and R2 of {sample_id=}")
        # fmt: on

        return merged_file

    @time_execution
    def run_parallel_meta(self):
        self.logger.info("Processing with Parallel Meta started")
        self.pm_output.mkdir(exist_ok=True)

        # fmt: off
        otu_abundance_command = [
            str(self.pm_path / "PM-pipeline"), "-i", str(self.seqs_list_file), "-m", str(self.meta_file), "-o",
            str(self.pm_output),
        ]
        if run_command(otu_abundance_command):
            self.logger.info("Successfully executed PM-pipeline (Step 1/4).")

        func_abundance_command = [
            str(self.pm_path / "PM-predict-func"), "-T", str(self.pm_output / "Abundance_Tables/taxa.OTU.Count"),
            "-o", str(self.pm_output / "Abundance_Tables/func"),
        ]
        if run_command(func_abundance_command):
            self.logger.info("Successfully executed PM-predict-func (Step 2/4).")

        for level in [2, 3]:
            select_func_command = [
                str(self.pm_path / "PM-select-func"), "-T",
                str(self.pm_output / f"Abundance_Tables/func.KO.Count"), "-o",
                str(self.pm_output / "Abundance_Tables/func"), "-L", str(level),
            ]
            if run_command(select_func_command):
                self.logger.info(f"Successfully executed PM-select-func -L {level} (Step {level+1}/4).")

        # fmt: on

    def analyze(self):
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
        self.logger.info(f"Successfully completed PM-meta batch analysis")
