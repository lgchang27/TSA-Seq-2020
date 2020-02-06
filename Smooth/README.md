# TSA-Seq data smoothing
This code is used to smooth the TSA-Seq enrichment scores (20kb bin) using the TSA-Seq_20kb.wig file from TSA-Seq normalization.

```shell
python TSA_smooth_hanningFor20kbNonsliding_TSA2.0.py --wig TSA-Seq_20kb.wig -w 20000 -aggwin 200000 --smooth -n1 TSA-Seq_hanning_20kbx21 -n2 TSA-Seq_hanning_20kbx21_agg_200kb -g utilities/hg38F.genome


#Genome size file hg38F.genome was for female cell line (K562), hg38M.genome was for male cell lines (H1, HCT116, HFFc6).
```

Figures 2e (top), 2f (top), Supplementary Figures 10a (top), 10b (top), 11a (top), 11b (top) were generated from the output bigwig file (TSA-Seq_hanning_20kbx21.bw) by this code.
