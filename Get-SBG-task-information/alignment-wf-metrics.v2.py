import sevenbridges as sbg
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--projectfile", help = "Required. A file that contants Cavatica project id. (Example: kfdrc-harmonization/sd-bhjxbdqk-03)", type = str, required = True)
parser.add_argument("-d", "--outdir", help = "Optional. Output directory. (default: ./)", type = str, required = False)
args = parser.parse_args()

base_url = 'https://cavatica-api.sbgenomics.com/v2/'
api = sbg.Api(url = base_url, token = os.environ['SB_AUTH_TOKEN'])

def get_align_metric(task, check):
    if task.outputs['aggregation_metrics'][0]:
        content = task.outputs['aggregation_metrics'][0].content()
        if check == 0:
            header = content.split("\n")[6]
            print >> align_file, "Project\tTask\t%s" % (header)
        for i in content.split("\n"):
            if '#' in i:
                continue
            if 'CATEGORY' in i:
                continue
            if 'PAIR' in i:
                print >> align_file, "%s\t%s\t%s" % (project, task.name, i)
        return 1
    else:
        print >> align_file, "%s\t%s" % (project, task.name)
        return check

def get_vcf_detail_metric(task, check):
    if task.outputs['gvcf_calling_metrics'][0]:
        content = task.outputs['gvcf_calling_metrics'][0].content()
        if check == 0:
            header = content.split("\n")[6]
            print >> vcf_d_file, "Project\tTask\t%s" % (header)
        print >> vcf_d_file, "%s\t%s\t%s" % (project, task.name, content.split("\n")[7])
        return 1
    else:
        print >> vcf_d_file, "%s\t%s" % (project, task.name)
        return check

def get_vcf_summary_metric(task, check):
    if task.outputs['gvcf_calling_metrics'][1]:
        content = task.outputs['gvcf_calling_metrics'][1].content()
        if check == 0:
            header = content.split("\n")[6]
            print >> vcf_s_file, "Project\tTask\t%s" % (header)
        print >> vcf_s_file, "%s\t%s\t%s" % (project, task.name, content.split("\n")[7])
        return 1
    else:
        print >> vcf_d_file, "%s\t%s" % (project, task.name)
        return check

def get_wgs_metric(task, check):
    if task.outputs['wgs_metrics']:
        content = task.outputs['wgs_metrics'].content()
        if check == 0:
            header = content.split("\n")[6]
            print >> wgs_file, "Project\tTask\t%s" % (header)
        print >> wgs_file, "%s\t%s\t%s" % (project, task.name, content.split("\n")[7])
        return 1
    else:
        print >> wgs_file, "%s\t%s" % (project, task.name)
        return check

infile = open(args.projectfile, 'r')
pjt = infile.readlines()
# pjt = ['yuankun/kf-alignment-rerun']
outdir = args.outdir or '.'

align_file = open(outdir + '/align_metrics.txt', 'w')
wgs_file = open(outdir + '/wgs_metrics.txt', 'w')
vcf_d_file = open(outdir + '/vcf_detail_metrics.txt', 'w')
vcf_s_file = open(outdir + '/vcf_summary_metrics.txt', 'w')
align_metrics_header = 0
wgs_metrics_header = 0
vcf_d_metrics_header = 0
vcf_s_metrics_header = 0


for project in pjt:
    project = project.rstrip()
    if '#' in project:
        continue
    if project: ## skip empty line
        tasks = api.tasks.query(project = project, status = 'COMPLETED').all()
        for task in tasks:
            if task.batch:
                for child in task.get_batch_children().all():
                    align_metrics_header =  get_align_metric(child, align_metrics_header)
                    wgs_metrics_header = get_wgs_metric(child, wgs_metrics_header)
                    vcf_d_metrics_header = get_vcf_detail_metric(child, vcf_d_metrics_header)
                    vcf_s_metrics_header = get_vcf_summary_metric(child, vcf_s_metrics_header)
            else:
                align_metrics_header =  get_align_metric(task, align_metrics_header)
                wgs_metrics_header = get_wgs_metric(task, wgs_metrics_header)
                vcf_d_metrics_header = get_vcf_detail_metric(task, vcf_d_metrics_header)
                vcf_s_metrics_header = get_vcf_summary_metric(task, vcf_s_metrics_header)
