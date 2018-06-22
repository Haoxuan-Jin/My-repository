## alignment-wf-metrics.v2.py
### Introduction
alignment-wf-metrics.v2.py is a python script to get task information from Cavatica via API and merge them into metrics.
### Quick start
To run `alignment-wf-metrics.v2.py`, use a file contented **Project IDs** of Cavatica with `-p` option. And a output directory can be specified by `-d` option. The following is an example command to run this script:
`python2 alignment-wf-metrics.v2.py -p Input_Project_ID.txt -d kf_output`
File `Input_Project_ID.txt` contents project ID: **"kfdrc-harmonization/sd-46sk55a3"** and the script will generate four ouput files `align_metrics.txt`, `vcf_detail_metrics.txt`, `vcf_summary_metrics.txt` and `wgs_metrics.txt` in `kf_output` directory.
### Usage
`$ python2 alignment-wf-metrics.v2.py -h`
```
usage: alignment-wf-metrics.v2.py [-h] -p PROJECTFILE [-d OUTDIR]

optional arguments:
  -h, --help            show this help message and exit
  -p PROJECTFILE, --projectfile PROJECTFILE
                        Required. A file that contants Cavatica project id.
                        (Example: kfdrc-harmonization/sd-bhjxbdqk-03)
  -d OUTDIR, --outdir OUTDIR
                        Optional. Output directory. (default: ./)
```
