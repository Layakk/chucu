#!/usr/bin/python
################################################################################
#
#
#
#
# CSV format:
# path, rs, tm, resource, scandate, positives, total
################################################################################

####
# Import
######
import requests
import time
import os
import subprocess

####
# Constants
######
URL_UPLOAD = 'https://www.virustotal.com/vtapi/v2/file/scan'
URL_REPORT = 'https://www.virustotal.com/vtapi/v2/file/report'
UPX_RUNNING_CMD_FORMAT="./lk_generate_specimen.sh -i %s -o %s -f -s %d -t %d -p %d -c -r -m %s"
SLEEPTIME_EXCEEDED = 60
SLEEPTIME_FIRST    = 300
SLEEPTIME_AFTER    = 60
EXTENSION='.exe'

####
# Inputs 
######
#Absolute path
APIKEY='####### API KEY #######'
in_specimen_real='/path/to/my/program.exe'

OUTPUTDIR='/path/to/my/out_program.exe'
EXTENSION='.exe'

CSVFILE='/path/to/my/specimens.csv'

RS_ARR=[10, 100, 1000, 2000]
RS_ARR_TOP=[0, 10, 100, 1000]
TM_ARR=[1000, 3000, 7000, 10000, 20000, 30000]
JMPS=["3,5","5,7","5,10"]

####
# Process
######
tmp_specimen_basename=os.path.basename(in_specimen_real)
tmp_specimen_splited=os.path.splitext(tmp_specimen_basename)

if not os.path.exists(OUTPUTDIR):
    print("[INFO] Creating specimens directory on %s"%(OUTPUTDIR))
    os.makedirs(OUTPUTDIR)

out_specimen_base=OUTPUTDIR + tmp_specimen_splited[0]
print("[INFO] Staring to find a valid specimen for %s..."%(in_specimen_real))
for JMP_LIMITS in JMPS:
    for RS_TOP in RS_ARR_TOP:
        for RS in RS_ARR:
            for TM in TM_ARR:
                no_funciona=False
                out_specimen_path=out_specimen_base + "_s" + str(RS) + "_p" + str(RS_TOP) + "_t" + str(TM) + "_m" + JMP_LIMITS.replace(",","_") + EXTENSION
                out_specimen_name=os.path.basename(out_specimen_path)
                print("[INFO] Generating specimen...\n\t%s"%(out_specimen_path))
                print(UPX_RUNNING_CMD_FORMAT%(in_specimen_real, out_specimen_path, RS, TM, RS_TOP, JMP_LIMITS))

                upx_process = subprocess.Popen(UPX_RUNNING_CMD_FORMAT%(in_specimen_real, out_specimen_path, RS, TM, RS_TOP, JMP_LIMITS), shell=True)
                upx_process.wait()

                if upx_process.returncode != 0:
                    print "[WARNING] Generating process ends with error: %d"%(upx_process.returncode)
                    continue

                print("[INFO] Done!\n"); 

                print("[INFO] Uploading specimen to VT...")
        
                upload_params = {'apikey':APIKEY}
                upload_file = {'file': (out_specimen_name, open(out_specimen_path, 'rb')) }

                task_done = False
                sleep_time=0
                while( not task_done):
                    time.sleep(sleep_time)
                    try:
                        upload_response = requests.post(URL_UPLOAD, files=upload_file, params=upload_params)
                    except:
                        no_funciona = True 

                    print "[DEBUG] Checking response code..."
                    if(upload_response.status_code == 204):
                        print "[WARNING] You have exceeded the requests' number. Waiting a minute."
                        sleep_time = SLEEPTIME_EXCEEDED
                        continue
                    elif(upload_response.status_code != 200):
                        print "[ERROR] Unexpected server response while uploading specimen. Exiting..."
                        exit(1)

                    task_done=True    

                if(no_funciona == True):
                    print "[INFO] Can't upload. Skipping..." 
                    continue

                print "[INFO] Done!" 
                out_specimen_resource=upload_response.json()['resource']
                print "[INFO] VT resource is: %s"%(out_specimen_resource)

                print("[INFO] Getting specimen's report...")

                task_done = False
                sleep_time=SLEEPTIME_FIRST
                report_params = {'apikey':APIKEY, 'resource':out_specimen_resource}

                no_funciona=False
                while( not task_done):
                    print "[INFO] Waiting analisis for %s seconds"%(sleep_time) 
                    time.sleep(sleep_time)
                    
                    try:
                        report_response = requests.get(URL_REPORT, params=report_params)
                    except:
                        no_funciona = True 

                    print "[DEBUG] Checking response code..." 
                    if(report_response.status_code == 204):
                        sleep_time = SLEEPTIME_EXCEEDED
                        print "[WARNING] You have exceeded the requests' number. Waiting %s seconds."%(sleep_time)
                        continue
                    elif(report_response.status_code != 200):
                        print "[ERROR] Unexpected server response while getting report."
                        exit(1)

                    json_report = report_response.json()
                    if(json_report['response_code'] == -2):
                        sleep_time=SLEEPTIME_AFTER
                        print "[INFO] Scanning have not finished yet. Waiting for %d seconds"%(sleep_time) 
                        continue
                    elif(json_report['response_code'] == 1):
                        print "[INFO] Scan is done." 
                        task_done=True
                    else:
                        print "[ERROR] Unexpected server response while getting report. Exiting..."
                        exit(1)

                if(no_funciona == True):
                    print "[INFO] Can't get report. Skipping..." 
                    continue

                print "[INFO] Done!"

                print "[INFO] Saving results..." 

                # path, rs, tm, resource, scan_date, positives, total
                csv_line=out_specimen_path + ";" + str(RS) + ";" + str(RS_TOP) + ";" + str(TM) + ";" + JMP_LIMITS + ";" + out_specimen_resource + ";" + str(json_report['scan_date']) + ";" + str(json_report['positives']) + ";" + str(json_report['total']) + "\n"
                print "[DEBUG] CSV: %s"%(csv_line)

                with open(CSVFILE, "a") as f:
                    f.write(csv_line)
        
                print "[INFO] Done!"


print "[INFO] Finishing..."
exit(0) 


