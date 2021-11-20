from db_functions import check_db_connection
from db_functions import get_connection
from db_functions import create_database
import json
import os
import re
from os import listdir
from os.path import isfile, join
import mysql.connector
from mysql.connector import errorcode

CVE_FILENAME = "vulInfo.txt"
OUTPUT_FILENAME = "results.P"
VICTIM_FILENAME = "accountinfo.P"
NVDPATH = "nvd_json_files"
DEFAULT_VALUE = "Undefined"
DB_NAME = "nvd"


def main():
    try:
        cves_f = open(CVE_FILENAME, 'r')
        cve_lines = cves_f.readlines()
        write_tuples(cve_lines)

    finally:
        cves_f.close()

def write_tuples(cve_lines):
    cve_id = "";
    lose_types = "";
    range_types = "";
    vuln_soft = "";
    severity = "";
    access = "";
    port = "";
    protocol = "";
    host = ""; 
    cve = "";
    
    hosts = []
    i = 0
    try:
        conn = get_connection()
        cursor = conn.cursor()
        while i < len(cve_lines):
            host = cve_lines[i].strip()
            if host not in hosts:
                hosts.append(host)
            cve = cve_lines[i+1].strip()
            port = cve_lines[i+2].strip()
            protocol = cve_lines[i+3].strip()
            query = "SELECT * FROM nvd WHERE id='{}'".format(cve.strip())
            query = query.strip()
            print("QUERY: {}".format(query))
            cursor.execute(query)
            cve_output = cursor.fetchall()
            if len(cve_output) == 0:
                print("CONTINUE")
                i = i+4
                continue
            cve_id, vuln_soft, range_types, lose_types, severity, access = cve_output[0]
            if ("remoteExploit" in range_types) and ("user_action_req" not in range_types):
                tup = "vuln_exists('" + host + "','" + cve_id + "'," + vuln_soft + ",[" +  \
                      range_types +"],[" + lose_types +"],'" + severity + "','" + access + "','" + port + \
                      "','" + protocol + "').\n"
            else:
                tup = "vuln_exists('" + host + "','" + cve_id + "'," + vuln_soft + ",[" +  \
                      range_types + "],[" + lose_types + "],'" + severity + "','" + access + "').\n" 
            print("TUP: {}".format(tup))
            with open(OUTPUT_FILENAME, "a") as f:
                f.writelines(tup)
            i = i+4

        print("HOSTS: {}".format(hosts))
        write_account(hosts)
    except IOError as err:
            print(err)


def write_account(hosts):
    try:
        for host in hosts:
            victim = "'" + host + "_victim'"
            compentent = "inCompetent({}).\n".format(victim)
            account = "hasAccount({},'{}',user).\n".format(victim, host)
            attacker_location = "attackerLocated(internet).\n"
            attacker_goal = "attackGoal(execCode('{}',_)).\n".format(host)
            with open(VICTIM_FILENAME, "a") as f:
                f.writelines(compentent)
                f.writelines(account)
                f.writelines(attacker_location)
                f.writelines(attacker_goal)
    except IOError as err:
        print(err)

        
main()
