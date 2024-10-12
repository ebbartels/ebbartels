import pandas as pd
import netaddr
import re
from bisect import bisect


ips = pd.read_csv("ip2location.csv")



def lookup_region(ip):
    global ips
    sub_ip = re.sub(r"[a-z]", "0", ip)
    number_ip = int(netaddr.IPAddress(sub_ip)) 
    
    idx = bisect(ips['low'], number_ip) - 1
    return ips.at[idx, "region"]

class Filing:
    def __init__(self, html):
        self.dates = re.findall(r"(19\d+|20\d+)-(0[1-9]|1[1-2])-(0[1-9]|1[1-9]|2[2-9]|3[0-1])", html)
        sic = re.findall(r"SIC=(\d+)", html)
        if sic:
            self.sic = int(sic[0])
        else:
            self.sic = None
        self.addresses = []
        addr_html = re.findall(r'<div class="mailer">([\s\S]+?)</div>', html)
        length = len(addr_html)
        for i in range(length):
            lines_addr = re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html[i])
            list_lines = []
            for line in lines_addr:
                list_lines.append(line.strip())
            full_addr = '\n'.join(list_lines)
            if len(full_addr) > 0:
                self.addresses.append(full_addr)

    def state(self):
        for address in self.addresses:
            state = re.findall(r'\s([A-Z]{2})\s\d{5}', address)
            if state:
                return state[0]
            else:
                return None

    
    

