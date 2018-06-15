#!/usr/bin/env python2
import sevenbridges as sbg
from datetime import datetime
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--project", help = "Cavatica project name. (Example: kfdrc-harmonization/sd-bhjxbdqk-03)", type = str, required = True)
parser.add_argument("-wt","--waittime", help = "Waitting time(seconds) of self-recheck for each time. (Default: 3600 seconds)", type = int, required = False)
parser.add_argument("-o","--outputlog", help = "Output log file. (Default: sbg_task_monitor.log)", type = str, required = False)

args = parser.parse_args()

# c = sbg.Config(profile='cavatica')
# api = sbg.Api(config=c)
base_url = 'https://cavatica-api.sbgenomics.com/v2/'
api = sbg.Api(url = base_url, token = os.environ['SB_AUTH_TOKEN'])
# api = sbg.Api(url = os.environ['SB_API_ENDPOINT'], token = os.environ['SB_AUTH_TOKEN'])

project = args.project
waittime = args.waittime or 3600
logfile = args.outputlog or 'sbg_task_monitor.log'

run = list()
draft = list()
log = open(logfile, 'w+')

## first check
tasks = api.tasks.query(project=project).all()
for task in tasks:
    if "RUNNING" in task.status:
        run.append(task)
    if "DRAFT" in task.status:
        draft.append(task)
run_num = len(run)
draft_num = len(draft)

## start self-recheck
while len(draft) >0:
    ## keep num of running tasks smaller than 200
    if run_num < 200:
        for u in draft[:]:
            u.run()
            log.write("Task: \"%s\" start running at %s\n" % (u.name, str(datetime.now())))
            # print (u.name,"start running",str(datetime.now()))
            draft.remove(u)
            run_num = run_num + 1
            if run_num == 200:
                break
            if len(draft) <1:
                break
    else:
        log.write("200 tasks are running at %s\n" % (str(datetime.now())))
        # print ("200 tasks are running",str(datetime.now()))
    
    ##default wait for an hour and start next loop.
    if len(draft) > 0:
        time.sleep(waittime)
        run = list()
        tasks = api.tasks.query(project=project).all()
        for task in tasks:
            if "RUNNING" in task.status:
                run.append(task)
        run_num = len(run)
log.write("No draft task in project: \"%s\" at %s\nMonitor exit.\n" % (project, str(datetime.now())))
# print ("No draft task in the project",str(datetime.now()))