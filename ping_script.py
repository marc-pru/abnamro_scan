import re
import os
import subprocess
import json
from pprint import pprint
import time
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d%H%M")
hostnames_and_ip_addresses = []


def check_host_reachable(ping_wan_output, print_output = False):
# returns a boolean value (true/false) to indicate that a remote IP is reachable or not
    if print_output:
        print()
        print(ping_wan_output)
        print()
    if "100% packet loss" in ping_wan_output:
        peering_status_ok = False
    elif "0% packet loss" in ping_wan_output:
        peering_status_ok = True
    else: peering_status_ok = False
    return peering_status_ok

def fetch_ip_address(ping_wan_output):
    if re.search(r'.+\s\S(\d+.\d+.\d+.\d+)',ping_wan_output, flags=re.IGNORECASE):
        ip_address = re.search(r'.+\s\S(\d+.\d+.\d+.\d+)',ping_wan_output, flags=re.IGNORECASE).group(1) 
    return(ip_address)


if __name__ == "__main__":
    fin = open('nodes_to_be_pinged.txt','rt')
    nodes_to_be_pinged_string = fin.read()
    nodes_to_be_pinged = nodes_to_be_pinged_string.splitlines()
    amount_of_nodes_finished = 0
    fin.close()
    print('\n'*40)
    print('{:<30}'.format('>'*30)+'{:^40}'.format('CHECK REACHABILITY SCRIPT')+'{:>30}'.format('<'*30))
    print('{:^104}'.format('This script will send an ICMP echo (ping) to the list of indicated nodes and fetch the IP-address'))
    print('{:<52}'.format('>'*52)+'{:>52}'.format('<'*52))
    print('\n'*5)
    reachability_report = {}

    for host in nodes_to_be_pinged:
        temp  = os.popen('ping -c 1 {}'.format(host))
        command_output = []
        for line in temp:
            command_output.append(line) 
        if len(command_output) == 0:
            is_reachable = False
            ip = "unknown"
        else: 
            is_reachable = check_host_reachable(command_output[4], False)
            ip = fetch_ip_address(command_output[0])
        if is_reachable: 
            reachability_report[host] = ("ip address: {}".format(ip), "Status = Reachable")
            hostnames_and_ip_addresses.append(host + ' ' + ':' +' ' + ip)
        else: reachability_report[host] = ("ip address: {}".format(ip), "Status = Unreachable")

        reachability_report_json = json.dumps(reachability_report, sort_keys=True, indent=4)
        fout1 = open('reachability_report.json', 'wt')
        fout1.write(reachability_report_json)
        fout1.close()
    print(hostnames_and_ip_addresses)
    hostnames_and_ip_addresses.sort()
    print(hostnames_and_ip_addresses)
    hostnames_and_ip_addresses_sort = ''
    for item in hostnames_and_ip_addresses:
        hostnames_and_ip_addresses_sort += item + '\n'
    fout2 = open('list_of_hostnames_and_ip_addresses.txt', 'wt')
    fout2.write(hostnames_and_ip_addresses_sort)
    fout2.close()
