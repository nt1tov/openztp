# -*- coding: utf-8 -*-
import logging
import os

logger = logging.getLogger("wrt.script")


def main(args):
    if args.list:
        return list(args)
    else:
        print(args)


def list(args):
    import os
    for s in os.listdir("scripts"):
        print(s)


def run(args):
    import os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "openwrt.settings")
    from django.core.wsgi import get_wsgi_application
    get_wsgi_application()
    from inventory.models import Device
    devs = Device.objects.filter()
    devs = devs.filter(pk__in=args.target).values_list('last_ip', flat=True)
    #for ip in devs:
        # print (f'running {args.name} {d} {" ".join(args.params)}')
    ssh('192.168.56.169', args.name, args.params)


def ssh(host, script, params):
    from pexpect import pxssh, EOF
    params = ' '.join(params)
    # print (script, params)
    logger.info(f'running script {script} {params}')
    os.system(f'scp -q scripts/{script} root@{host}:/tmp')
    try:
        s = pxssh.pxssh(timeout=60, options={
                    "StrictHostKeyChecking": "no"})
        s.login(host, 'root', )
        s.sendline(f'sh /tmp/{script} {params}')   # run a command
        s.prompt()             # match the prompt
        # print(s.before)        # print everything before the prompt
        logger.debug(s.before)
        s.logout()
    except pxssh.ExceptionPxssh as e:
        print("pxssh failed on login.")
        print(e)
    except EOF:
        pass
        #logger.debug("pexpect EOF")
