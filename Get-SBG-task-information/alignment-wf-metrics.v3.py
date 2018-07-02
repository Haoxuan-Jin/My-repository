import sevenbridges as sbg
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--projectfile", help = "Required. A file that contants Cavatica project id. (Example: kfdrc-harmonization/sd-bhjxbdqk-03)", type = str, required = True)
parser.add_argument("-d", "--outdir", help = "Optional. Output directory. (default: ./)", type = str, required = False)
args = parser.parse_args()

base_url = 'https://cavatica-api.sbgenomics.com/v2/'
api = sbg.Api(url = base_url, token = os.environ['SB_AUTH_TOKEN'])


def get_align_metric(task):
    if task.outputs['aggregation_metrics'][0]:
        content = task.outputs['aggregation_metrics'][0].content()
        header = content.split("\n")[6].split("\t")
        for i in content.split("\n"):
            if '#' in i:
                continue
            if 'CATEGORY' in i:
                continue
            if 'PAIR' in i:
                j = 0
                for k in i.split("\t"):
                    df[task.name][header[j]] = k
                    j = j + 1
        return 1
    # else:
    #     print >> align_file, "%s\t%s" % (project, task.name)
        # return check

def get_vcf_summary_metric(task):
    if task.outputs['gvcf_calling_metrics'][0]:
        content = task.outputs['gvcf_calling_metrics'][0].content()
        header = content.split("\n")[6].split("\t")
        j = 0
        for i in content.split("\n")[7].split("\t"):
            df[task.name][header[j]] = i
            j = j + 1
        return 1
    # else:
    #     print >> vcf_d_file, "%s\t%s" % (project, task.name)
    #     return check

def get_wgs_metric(task):
    if task.outputs['wgs_metrics']:
        content = task.outputs['wgs_metrics'].content()
        header = content.split("\n")[6].split("\t")
        j = 0
        for i in content.split("\n")[7].split("\t"):
            df[task.name][header[j]] = i
            j = j + 1
        return 1
    # else:
    #     print >> wgs_file, "%s\t%s" % (project, task.name)
    #     return check

infile = open(args.projectfile, 'r')
pjt = infile.readlines()
# pjt = ['yuankun/kf-alignment-rerun']
outdir = args.outdir or '.'
outfile = outdir + '/alignment-wf-all-summary-metrics.csv'

df = {}
for project in pjt:
    project = project.rstrip()
    if '#' in project:
        continue
    if project: ## skip empty line
        tasks = api.tasks.query(project = project, status = 'COMPLETED').all()
        for task in tasks:
            if task.batch:
                for child in task.get_batch_children().all():
                    df[child.name] = {
                        'Project': project,
                        'Task': child.name
                    }
                    align_metrics_header =  get_align_metric(child)
                    wgs_metrics_header = get_wgs_metric(child)
                    vcf_s_metrics_header = get_vcf_summary_metric(child)
            else:
                df[task.name] = {
                    'Project': project,
                    'Task': task.name
                }
                align_metrics_header =  get_align_metric(task)
                wgs_metrics_header = get_wgs_metric(task)
                vcf_s_metrics_header = get_vcf_summary_metric(task)

metric = pd.DataFrame.from_dict(df)
metric = metric.T
metric.to_csv(outfile)
