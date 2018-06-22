import sevenbridges as sbg
import os

base_url = 'https://cavatica-api.sbgenomics.com/v2/'
api = sbg.Api(url = base_url, token = os.environ['SB_AUTH_TOKEN'])

def get_align_metric(task, check):
    content = task.outputs['collect_collect_aggregation_metrics'][0].content()
    if check == 0:
        header = content.split("\n")[6]
        print >> align_file, "Project\tTask\t%s" % (header)
    for i in content.split("\n"):
        if '#' in i:
            continue
        if 'CATEGORY' in i:
            continue
        if 'PAIR' in i:
            print >> align_file, "%s\t%s\t%s" % (pjt, task.name, i)
    return 1

def get_vcf_detail_metric(task, check):
    content = task.outputs['picard_collect_gvcf_calling_metrics'][0].content()
    if check == 0:
        header = content.split("\n")[6]
        print >> vcf_d_file, "Project\tTask\t%s" % (header)
    print >> vcf_d_file, "%s\t%s\t%s" % (pjt, task.name, content.split("\n")[7])
    return 1

def get_vcf_summary_metric(task, check):
    content = task.outputs['picard_collect_gvcf_calling_metrics'][0].content()
    if check == 0:
        header = content.split("\n")[6]
        print >> vcf_s_file, "Project\tTask\t%s" % (header)
    print >> vcf_s_file, "%s\t%s\t%s" % (pjt, task.name, content.split("\n")[7])
    return 1

def get_wgs_metric(task, check):  
    content = task.outputs['collect_wgs_metrics'].content()
    if check == 0:
        header = content.split("\n")[6]
        print >> wgs_file, "Project\tTask\t%s" % (header)
    print >> wgs_file, "%s\t%s\t%s" % (pjt, task.name, content.split("\n")[7])
    return 1

pjt = 'yuankun/kf-alignment-rerun'
tasks = api.tasks.query(project = pjt, status = 'COMPLETED').all()
align_file = open('align_metrics.txt', 'w')
wgs_file = open('wgs_metrics.txt', 'w')
vcf_d_file = open('vcf_detail_metrics.txt', 'w')
vcf_s_file = open('vcf_summary_metrics.txt', 'w')
align_metrics_header = 0
wgs_metrics_header = 0
vcf_d_metrics_header = 0
vcf_s_metrics_header = 0
for task in tasks:
    if task.batch:
        for child in task.get_batch_children().all():
            align_metrics_header =  get_align_metric(child, align_metrics_header)
            wgs_metrics_header = get_wgs_metric(child, wgs_metrics_header)
            vcf_d_metrics_header = get_vcf_detail_metric(child, vcf_d_metrics_header)
            vcf_s_metrics_header = get_vcf_summary_metric(child, vcf_s_metrics_header)
    else:
        align_metrics_header =  get_align_metric(child, align_metrics_header)
        wgs_metrics_header = get_wgs_metric(child, wgs_metrics_header)
        vcf_d_metrics_header = get_vcf_detail_metric(child, vcf_d_metrics_header)
        vcf_s_metrics_header = get_vcf_summary_metric(child, vcf_s_metrics_header)
