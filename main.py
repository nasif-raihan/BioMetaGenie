import argparse
from service import PMBatchAnalyzer, NcbiSraDownloader, TrimGaloreTrimmer

# Initialize instances
ncbi_sra_downloader = NcbiSraDownloader()
trim_galore_trimmer = TrimGaloreTrimmer()
pm_batch_analyzer = PMBatchAnalyzer()

# Argument parser setup
parser = argparse.ArgumentParser(description="SRA Sample Pre-processing CLI")

subparsers = parser.add_subparsers(dest="command")

# Sub-command for downloading a single SRA
download_sra_parser = subparsers.add_parser(
    "download_sra", help="Download a single SRA file."
)
download_sra_parser.add_argument(
    "srr_id", type=str, help="SRR ID for the SRA file to download."
)

# Sub-command for converting a single SRA to FASTQ
convert_fastq_parser = subparsers.add_parser(
    "convert_to_fastq", help="Convert a single SRA file to FASTQ format."
)
convert_fastq_parser.add_argument(
    "srr_id", type=str, help="SRR ID for the SRA file to convert."
)

# Sub-command for downloading and converting multiple SRA files to FASTQ
process_sra_list_parser = subparsers.add_parser(
    "process_sra_list", help="Download and convert multiple SRA files to FASTQ."
)

# Sub-command for trimming FASTQ files
trim_parser = subparsers.add_parser(
    "trim", help="Trim all FASTQ sequences in the directory."
)

# Sub-command for getting sequence statistics of trimmed FASTQ files
stats_parser = subparsers.add_parser(
    "get_sample_stats", help="Get sequence statistics of all trimmed FASTQ files."
)

# Sub-command for merging R1 and R2 reads
merge_reads_parser = subparsers.add_parser(
    "merge_reads", help="Merge R1 and R2 reads for a sample."
)
merge_reads_parser.add_argument(
    "sample_id", type=str, help="Sample ID for merging reads."
)

# Sub-command for performing PM-Meta batch analysis
analyze_parser = subparsers.add_parser(
    "analyze", help="Perform PM-Meta batch analysis."
)

# Parse the arguments
args = parser.parse_args()

# Execute based on the command
if args.command == "download_sra":
    ncbi_sra_downloader.download_sra(srr_id=args.srr_id)
elif args.command == "convert_to_fastq":
    ncbi_sra_downloader.convert_to_fastq(srr_id=args.srr_id)
elif args.command == "process_sra_list":
    ncbi_sra_downloader.process_sra_list()
elif args.command == "trim":
    trim_galore_trimmer.trim()
elif args.command == "get_sample_stats":
    trim_galore_trimmer.get_sample_stats()
elif args.command == "merge_reads":
    pm_batch_analyzer.merge_reads(sample_id=args.sample_id)
elif args.command == "analyze":
    pm_batch_analyzer.analyze()
else:
    ncbi_sra_downloader.process_sra_list()
    trim_galore_trimmer.trim()
    pm_batch_analyzer.analyze()
