from service import PMBatchAnalyzer, NcbiSraDownloader, TrimGaloreTrimmer

ncbi_sra_downloader = NcbiSraDownloader()
trim_galore_trimmer = TrimGaloreTrimmer()
pm_batch_analyzer = PMBatchAnalyzer()

ncbi_sra_downloader.process_sra_list()
trim_galore_trimmer.trim()
pm_batch_analyzer.analyze()
