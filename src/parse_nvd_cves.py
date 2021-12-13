from db_functions import check_db_connection
from db_functions import get_connection
from db_functions import create_database
import json
import re
from os import listdir
from os.path import isfile, join
import mysql.connector
from mysql.connector import errorcode

NVDPATH = "nvd_json_files"
DEFAULT_VALUE = "Undefined"
DB_NAME = "nvd"

nvd_files = [f for f in listdir(NVDPATH) if isfile(join(NVDPATH, f))]
print(nvd_files)

conn = get_connection()
cursor = conn.cursor()
cursor.execute("USE {}".format(DB_NAME))

for f in nvd_files:
    f = open(join(NVDPATH,f))
    json_object = json.load(f)
    
    for cve_item in json_object['CVE_Items']:
        # get CVE-ID
        cve_id = cve_item['cve']['CVE_data_meta']['ID']
        severity = DEFAULT_VALUE
        access = DEFAULT_VALUE
        lose_types = ""
        range_types = ""
        vuln_soft = DEFAULT_VALUE
       
        if 'baseMetricV2' in cve_item['impact']:
            # get severity level
            severity = cve_item['impact']['baseMetricV2']['severity']
            # get access level
            vector_string = cve_item['impact']['baseMetricV2']['cvssV2']['vectorString']
            access = re.split(':|/', vector_string)[3].lower()
            # get lose types
            availability_loss = cve_item['impact']['baseMetricV2']['cvssV2']['availabilityImpact']
            data_loss = cve_item['impact']['baseMetricV2']['cvssV2']['confidentialityImpact']
            integrity_loss = cve_item['impact']['baseMetricV2']['cvssV2']['integrityImpact']

            if availability_loss != "NONE":
                lose_types += "'availability_loss',"
            if data_loss != "NONE":
                lose_types += "'data_loss',"
            if integrity_loss != "NONE":
                lose_types += "'data_modification',"
            
            lose_types = lose_types[:-1]
            # get range level
            if 'userInteractionRequired' in cve_item['impact']['baseMetricV2']:
                user_action_required = cve_item['impact']['baseMetricV2']['userInteractionRequired']
            access_vector = cve_item['impact']['baseMetricV2']['cvssV2']['accessVector']
            if user_action_required:
                range_types += "'user_action_req',"
            if access_vector == "LOCAL":
                range_types += "'lan',"
            elif access_vector == "ADJACENT_NETWORK":
                range_types += "'remoteExploit',"
            elif access_vector == "NETWORK":
                range_types += "'local',"
            
            range_types = range_types[:-1]
            # get vulnerable software
            node_list = cve_item['configurations']['nodes']
            for node in node_list:
                if 'cpe_match' in node:
                    cpe_list = node['cpe_match']
                    for cpe_item in cpe_list:
                        cpe_item = cpe_item['cpe23Uri']
                        vuln_soft = cpe_item.split(":")[4]
                        break
                break
            vuln_soft = "'" + vuln_soft + "'"
            

        print("CVE-ID: {}, Severity: {}, Access: {}, Lose Types: {}, Range Types: {}, Vulnerable Software: {}".format(cve_id, severity, access, lose_types, range_types, vuln_soft))

        add_cve = ("INSERT INTO nvd "
                  "(id, soft, rng, lose_types, severity, access) "
                  "VALUES (%s, %s, %s, %s, %s, %s)")

        cve_data = (cve_id, vuln_soft, range_types, lose_types, severity, access)
 
        cursor.execute(add_cve, cve_data)
        conn.commit()


cursor.close()
conn.close()

