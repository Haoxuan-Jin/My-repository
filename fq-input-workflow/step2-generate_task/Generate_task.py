import sevenbridges as sbg
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-pjt", required=True)
parser.add_argument("-input_file", required=True)
args = parser.parse_args()

# c = sbg.Config(profile='cavatica')
# api = sbg.Api(config=c)
base_url = 'https://cavatica-api.sbgenomics.com/v2/'
api = sbg.Api(url = base_url, token = os.environ['SB_AUTH_TOKEN'])
# api = sbg.Api(url = os.environ['SB_API_ENDPOINT'], token = os.environ['SB_AUTH_TOKEN'])

project = args.pjt

# app = project + '/kfdrc-alignment-workflow'
app = project + '/kf-alignment-fq-input-wf'

f = open (args.input_file)

for line in f.readlines():  
    line=line.split()
    name = 'alignment-' + line[-1] 
    inputs={}
    inputs['contamination_sites_bed'] = api.files.query(project=project, names=["Homo_sapiens_assembly38.contam.bed"])[0]
    inputs['contamination_sites_mu'] = api.files.query(project=project, names=["Homo_sapiens_assembly38.contam.mu"])[0]
    inputs['contamination_sites_ud'] = api.files.query(project=project, names=["Homo_sapiens_assembly38.contam.UD"])[0]
    inputs['dbsnp_vcf'] = api.files.query(project=project, names=["Homo_sapiens_assembly38.dbsnp138.vcf"])[0]
    inputs['indexed_reference_fasta'] = api.files.query(project=project, names=["Homo_sapiens_assembly38.fasta"])[0]

    ### special for fq input
    fq1 = []
    fq2 = []
    rgs = []
    count = (len(line) - 1) / 3
    for i in range(0,count):
        r1 = i * 3 
        r2 = i * 3 + 1 
        rg = i * 3 + 2
        fq1.append(line[r1])
        fq2.append(line[r2])
        rgs.append(line[rg])
    # inputs['files_R1'] = api.files.query(project=project, names=[fq1[0]])[0]
    # inputs['files_R2'] = api.files.query(project=project, names=[fq2[0]])[0]
    inputs['files_R1'] = api.files.query(project=project, names=fq1)
    inputs['files_R2'] = api.files.query(project=project, names=fq2)
    # print(list(inputs['files_R1']))

    # inputs['input_reads'] = api.files.query(project=project, names=[line[0]])[0]
    inputs['knownsites'] = api.files.query(project=project, names=["1000G_omni2.5.hg38.vcf.gz","1000G_phase1.snps.high_confidence.hg38.vcf.gz","Homo_sapiens_assembly38.known_indels.vcf.gz","Mills_and_1000G_gold_standard.indels.hg38.vcf.gz"])
    inputs['reference_dict'] = api.files.query(project=project, names=["Homo_sapiens_assembly38.dict"])[0]
    inputs['wgs_calling_interval_list'] = api.files.query(project=project, names=["wgs_calling_regions.hg38.interval_list"])[0]
    inputs['wgs_coverage_interval_list'] = api.files.query(project=project, names=["wgs_coverage_regions.hg38.interval_list"])[0]
    inputs['wgs_evaluation_interval_list'] = api.files.query(project=project, names=["wgs_evaluation_regions.hg38.interval_list"])[0]
    inputs['output_basename'] = line[-1]
    inputs['rgs'] = rgs
    try:
        task = api.tasks.create(name=name, project=project, app=app, inputs=inputs, run=False)
        task.inputs['output_basename'] = task.id
        task.save()
        # print (task.inputs[''].name,task.inputs['rgs'],task.id)
    except:
        print('I was unable to run the task.')