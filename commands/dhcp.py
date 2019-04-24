# -*- coding: utf-8 -*-

import os, json
from collections import defaultdict
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwrt.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

def lease(args):
    from dhcp.models import Lease
    from provisioning.models import Device

    Lease.close(mac=args.mac)
    ip = args.ip
    mac = args.mac
    hostname = args.hostname
    start = args.start
    end = args.end
    lease = Lease(ip=ip, mac=mac, hostname=hostname, start=start, end=end)
    lease.save()

    # check device
    mac = lease.mac
    dev = Device.objects.filter(mac=mac)
    if not dev.exists():
        dev = Device(mac=mac, hostname=lease.hostname, last_ip=lease.ip)
        dev.save()

def show(args):
    from dhcp.models import Lease
    print ('MAC\t\tIP\t\tHOSTNAME\tSTART\t\tEND')
    for l in Lease.objects.all():
        print (f'{l.mac}\t{l.ip}\t{l.hostname}\t{l.start}\t{l.end}')
