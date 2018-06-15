awk -F ',' '{print $2"\t"$18}' Normal-wgs-fq-manifest.csv|grep -v 'name' > WGS_normal_fq-uuid.lst
perl get_wgs_fq.pl WGS_normal_fq-uuid.lst > CBTTC.BSID.wgs.normal.txt
