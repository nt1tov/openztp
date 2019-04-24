# -*- coding: utf-8 -*-
from commands.script import ssh
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwrt.settings")
get_wsgi_application()
from inventory.models import Device
import logging


logger = logging.getLogger("wrt.device")


def main(args):
    print(args)


def list(args):
    print('ID\tMAC\t\t\tIP\t\tHOSTNAME\tVERSION')
    devs = Device.objects.filter()
    if args.ip:
        devs = devs.filter(ip=args.ip)
    if args.mac:
        devs = devs.filter(mac=args.mac)
    if args.hostname:
        devs = devs.filter(hostname=args.hostname)
    for d in devs:
        print(f'{d.pk}\t{d.mac}\t{d.last_ip}\t{d.hostname}\t\t{d.firmware}')


def show(args):
    try:
        d = Device.objects.get(pk=args.id)
        print(f'ID\t\t: {d.pk}')
        print(f'MAC\t\t: {d.mac}')
        print(f'IP\t\t: {d.last_ip}')
        print(f'HOSTNAME\t: {d.hostname}')
        print('-'*16)
        print(f'VERSION\t\t: 1234')
        print(f'TUNNEL\t\t: 1234')

    except Device.DoesNotExist:
        pass


def remove(args):
    try:
        d = Device.objects.get(pk=args.id)
        d.delete()
    except Device.DoesNotExist:
        pass


def register(mac, hostname, ip, release):
    dev = Device.objects.filter(mac=mac)
    if dev.exists():
        dev = dev.get()
        update = dict()
        if dev.last_ip != ip:
            dev.ip = ip
            update['ip'] = ip
        if dev.hostname != hostname:
            dev.hostname = hostname
            update['hostname'] = hostname
        if dev.firmware != release:
            dev.firmware = release
            update['firmware'] = release
        if update:
            dev.save()
            logger.info(f'updating device {dev.pk}: {update}')
    else:
        dev = Device(
            mac=mac,
            hostname=hostname,
            last_ip=ip,
            firmware=release
        )
        dev.save()
        logger.info(f'registered new device {dev.pk}: {ip} {mac} {hostname} {release}')

        # init new device
        logger.info(f'init device {dev.pk}')
        ssh(
            ip,
            'init.sh',
            [f'{dev.pk}']
        )
