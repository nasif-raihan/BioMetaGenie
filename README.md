# BioMetaGenie

BioMetaGenie is an advanced bioinformatics toolkit designed to streamline and integrate the processes of downloading, processing, and analyzing genomic data. By consolidating multiple powerful tools into a single, user-friendly interface, BioMetaGenie provides an efficient end-to-end workflow for genomic data management.

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
   - Install the required tools:
     - SRA Toolkit
     - Seqkit
     - Usearch11
     - TrimGalore
     - Parallel Meta
   - Execute the setup script:
     ```bash
     cd third_party
     bash setup.sh
     ```

4. **Make Usearch11 Executable**:
   ```bash
   chmod +x usearch11.0.667_i86linux32
   cd ..
   ```

5. **Configuration**:
   - Place your sample names or SRA accession numbers in the `SRA_list.txt` file located in the `input` directory.

## Usage

BioMetaGenie simplifies complex workflows into a single command. After installation, run the following command to execute the entire process:

```bash
make run
```

## Contributing

We welcome contributions to BioMetaGenie! To contribute, please fork the repository and submit a pull request. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

BioMetaGenie is released under the MIT License. For details, see the [LICENSE](LICENSE) file.

## Contact

For support or inquiries, please use the [Issues](https://github.com/nasif-raihan/BioMetaGenie/issues) section on GitHub.

---

BioMetaGenie is committed to simplifying and accelerating genomic data processing, enabling researchers to concentrate on their analyses rather than on data management tasks.

