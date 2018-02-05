#!/usr/bin/python

import dns.resolver #import the module
import dns.exception
import sys
import threading
import csv
from datetime import datetime
from pytz import timezone

num = 0
def get_IP(dnssv, sub_dnssv, targetDomain):
    fp = open('save_file.csv', 'ab')
    wr = csv.writer(fp)
    timer = threading.Timer(3600, get_IP, args=[dnssv, sub_dnssv, targetDomain])
    global num
    res = dns.resolver.Resolver()

    try:
        res.nameservers = [dnssv]
        answers = res.query(targetDomain)
    except (dns.resolver.Timeout, dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers):
        res.nameservers = [sub_dnssv]
        answers = res.query(targetDomain)

    for rdata in answers:
        Time_now = datetime.now(timezone('Asia/Seoul'))
        wr.writerow([num, Time_now, targetDomain, rdata.address, res.nameservers[0]])
        num = num +1
    timer.start()
    fp.close()

def main(dnssv, sub_dnssv, targetDomain):
    get_IP(dnssv, sub_dnssv, targetDomain)

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print ('Enter "python Test_Dns.py <DNS> <Sub_DNS> <TargetDomain>"')
        sys.exit(1)

    dnssv = sys.argv[1]
    sub_dnssv = sys.argv[2]
    targetDomain = sys.argv[3]


    main(dnssv, sub_dnssv, targetDomain)

