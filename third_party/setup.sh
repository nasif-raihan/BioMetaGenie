#!/bin/bash

# shellcheck disable=SC2035
# shellcheck disable=SC2164

# Download SRA Toolkit
wget wget --output-document sratoolkit.tar.gz https://ftp-trace.ncbi.nlm.nih.gov/sra/sdk/current/sratoolkit.current-ubuntu64.tar.gz
tar -vxzf sratoolkit.tar.gz
export "PATH=$PATH:$(pwd)/sratoolkit.*/bin"  >> ~/.bashrc

# Download Seqkit
wget https://github.com/shenwei356/seqkit/releases/download/v2.3.1/seqkit_linux_amd64.tar.gz
tar -zxvf *.tar.gz
echo "export seqkit=$(pwd)/seqkit" >> ~/.bashrc


# Download usearch
wget https://www.drive5.com/downloads/usearch11.0.667_i86linux32.gz -O usearch
gunzip usearch11.0.667_i86linux32.gz
echo "export usearch=$(pwd)/usearch" >> ~/.bashrc

# Download Trim Galore
git clone https://github.com/FelixKrueger/TrimGalore
chmod +x TrimGalore/trim_galore
echo "export TrimGalore=$(pwd)/trim_galore" >> ~/.bashrc

# Download Parallel Meta
wget bioinfo.single-cell.cn/Released_Software/parallel-meta/3.7/parallel-meta-suite-3.7-src.tar.gz
tar -zxvf parallel-meta-suite-3.7-src.tar.gz
echo "export ParallelMETA=$(pwd)/parallel-meta-suite" >> ~/.bashrc
echo "export PATH=${PATH}:$(pwd)/parallel-meta-suite/bin" >> ~/.bashrc
cd parallel-meta-suite
make

