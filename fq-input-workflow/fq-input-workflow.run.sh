## get BS id
python2 get_bs_id.py > CBTTC.BSID.txt

## step1-get_WGS_fq
ln -s CBTTC.BSID.txt step1-get_WGS_fq/CBTTC.BSID.txt
awk -F ',' '{print $2"\t"$18}' Normal-wgs-fq-manifest.csv|grep -v 'name' > step1-get_WGS_fq/WGS_normal_fq-uuid.lst
perl step1-get_WGS_fq/get_wgs_fq.pl step1-get_WGS_fq/WGS_normal_fq-uuid.lst > step1-get_WGS_fq/CBTTC.BSID.wgs.normal.txt

## step2-generate_task
ln -s step1-get_WGS_fq/CBTTC.BSID.wgs.normal.txt step2-generate_task/CBTTC.BSID.wgs.normal.txt
python2 step2-generate_task/Generate_task.py -pjt kfdrc-harmonization/sd-bhjxbdqk-03 -input_file step2-generate_task/CBTTC.BSID.wgs.normal.txt

## step3-run_monitor_task
python2 step3-run_monitor_task/sbg_task_monitor.py -p kfdrc-harmonization/sd-bhjxbdqk-03 -wt 3600 -o step3-run_monitor_task/sbg_task_monitor.log