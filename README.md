# BioMetaGenie
![release-v1.0](https://img.shields.io/badge/release-v1.0-brightgreen)
![license-MIT](https://img.shields.io/badge/license-MIT-blue)

BioMetaGenie is an advanced bioinformatics toolkit designed to streamline and integrate the processes of downloading, 
processing, and analyzing genomic data. By consolidating multiple powerful tools into one intuitive CLI interface, 
BioMetaGenie provides an efficient end-to-end workflow for genomic data preprocessing, significantly easing 
the workload for researchers.

## Features

- **Efficient Data Retrieval**: Seamlessly download genomic data from NCBI using the SRA Toolkit.
- **Automated Conversion**: Effortlessly convert downloaded files to FASTQ format.
- **High-Quality Trimming**: Utilize TrimGalore for high-quality read trimming.
- **Detailed Sequence Reporting**: Generate detailed sequence status reports with Seqkit.
- **Read Merging**: Automatically merge paired-end reads into cohesive sequences.
- **In-Depth Analysis**: Leverage Parallel Meta for comprehensive sequence abundance and count analysis.

## Installation

To get started with BioMetaGenie, follow these instructions:

1. **Prerequisites**:
   - Ensure that [Poetry](https://python-poetry.org/docs/#installation) is installed for dependency management.

2. **Clone the Repository**:
   ```bash
   git clone https://github.com/nasif-raihan/BioMetaGenie.git
   cd BioMetaGenie
   ```

3. **Setup Third-Party Dependencies**:
   - Install the required tools by executing the setup script::
     - [SRA Toolkit](https://github.com/ncbi/sra-tools/wiki/02.-Installing-SRA-Toolkit)
     - [Seqkit](https://bioinf.shenwei.me/seqkit/download/)
     - [Usearch11](https://www.drive5.com/usearch/download.html)
     - [TrimGalore](https://github.com/FelixKrueger/TrimGalore)
     - [Parallel Meta](https://github.com/qdu-bioinfo/parallel-meta-suite)
     ```bash
     cd third_party
     bash setup-for-linux.sh
     ```
    Currently, the setup script only supports Linux distributions. Contributions are welcome to extend cross-platform 
    compatibility by creating `setup-for-win.sh` for Windows and `setup-for-mac.sh` for macOS. <br><br>
4. **Make Usearch11 Executable**:
   ```bash
   chmod +x usearch11.0.667_i86linux32
   cd ..
   ```

5. **Configuration**:
   - Place your sample names or SRA accession numbers in the `SRA_list.txt` file located in the `input` directory.

## Usage

BioMetaGenie simplifies complex workflows into a single command. 
After installation, run the following command from `root` directory _**(BioMetaGenie)**_ to execute the entire process:

```bash
    make install
    poetry shell
    make run
```

### Some other example usages:
- **Download SRA**: 
    ```bash
        python script.py download_sra SRR123456
    ```
- **Convert to FASTQ**: 
    ```bash
        python script.py convert_to_fastq SRR123456
    ```
- **Download and process a list**: 
    ```bash
        python script.py process_sra_list
    ```
- **Trim sequences**: 
    ```bash
        python script.py trim
    ```
- **Get sample stats**: 
    ```bash
        python script.py get_sample_stats
    ```
- **Merge reads**: 
    ```bash
        python script.py merge_reads sample123
    ```
- **Analyze**: 
    ```bash
        python script.py analyze
    ```

All the outputs will be stored in the `output` directory.

## Contributing

We welcome contributions to BioMetaGenie! To contribute, please fork the repository and submit a pull request. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

BioMetaGenie is released under the MIT License. For details, see the [LICENSE](LICENSE) file.

## Contact

For support or inquiries, please use the [Issues](https://github.com/nasif-raihan/BioMetaGenie/issues) section on GitHub.

---

BioMetaGenie is committed to simplifying and accelerating genomic data processing, enabling researchers to concentrate on their analyses rather than on data management tasks.

