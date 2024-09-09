#!/bin/bash

# shellcheck disable=SC2035
# shellcheck disable=SC2164
# shellcheck disable=SC1090
# shellcheck disable=SC2155
# shellcheck disable=SC2034

exec > >(tee -a $LOG_FILE) 2>&1  # Log all output to a file and print to console

echo "========== Starting Setup Script =========="
START_TIME=$(date)

# Download SRA Toolkit
echo "Downloading SRA Toolkit..."
if wget --output-document sratoolkit.tar.gz https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-ubuntu64.tar.gz; then
    echo "SRA Toolkit downloaded successfully."
else
    echo "Failed to download SRA Toolkit." >&2
    exit 1
fi

echo "Extracting SRA Toolkit..."
tar -vxzf sratoolkit.tar.gz
SRA_TOOLKIT_DIR=$(find "$(pwd)" -type d -name 'sratoolkit.*' | head -n 1)
export PATH="$PATH:$SRA_TOOLKIT_DIR/bin"
echo "export PATH=\"\$PATH:$SRA_TOOLKIT_DIR/bin\"" >> ~/.bashrc
echo "SRA Toolkit installation complete."

# Download Seqkit
echo "Downloading Seqkit..."
if wget https://github.com/shenwei356/seqkit/releases/download/v2.3.1/seqkit_linux_amd64.tar.gz; then
    echo "Seqkit downloaded successfully."
else
    echo "Failed to download Seqkit." >&2
    exit 1
fi

echo "Extracting Seqkit..."
tar -zxvf seqkit_linux_amd64.tar.gz
echo "export seqkit=$(pwd)/seqkit" >> ~/.bashrc
echo "Seqkit installation complete."

# Download usearch
echo "Downloading USEARCH..."
if wget https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz -O usearch; then
    echo "USEARCH downloaded successfully."
else
    echo "Failed to download USEARCH." >&2
    exit 1
fi

echo "Extracting USEARCH..."
gunzip usearch11.0.667_i86linux32.gz
echo "export usearch=$(pwd)/usearch" >> ~/.bashrc
echo "USEARCH installation complete."

# Download Trim Galore
echo "Downloading Trim Galore..."
if git clone https://github.com/FelixKrueger/TrimGalore; then
    echo "Trim Galore downloaded successfully."
else
    echo "Failed to download Trim Galore." >&2
    exit 1
fi

chmod +x TrimGalore/trim_galore
echo "export TrimGalore=$(pwd)/trim_galore" >> ~/.bashrc
echo "Trim Galore installation complete."

# Download Parallel Meta
echo "Downloading Parallel Meta..."
if wget bioinfo.single-cell.cn/Released_Software/parallel-meta/3.7/parallel-meta-suite-3.7-src.tar.gz; then
    echo "Parallel Meta downloaded successfully."
else
    echo "Failed to download Parallel Meta." >&2
    exit 1
fi

echo "Extracting Parallel Meta..."
tar -zxvf parallel-meta-suite-3.7-src.tar.gz
echo "export ParallelMETA=\"$(pwd)/parallel-meta-suite\"" >> ~/.bashrc
echo "export PATH=\"\$PATH:\$ParallelMETA/bin\"" >> ~/.bashrc
cd parallel-meta-suite

echo "Building Parallel Meta..."
if make; then
    echo "Parallel Meta built successfully."
else
    echo "Failed to build Parallel Meta." >&2
    exit 1
fi

# Apply changes to PATH
echo "Sourcing bashrc to apply PATH changes..."
source ~/.bashrc

echo "========== Setup Complete =========="
END_TIME=$(date)
echo "Start Time: $START_TIME"
echo "End Time: $END_TIME"
