#!/bin/sh
# set hostname
uci set system.@system[0].hostname='wrt'$1
uci commit system
/etc/init.d/system reload
# update
update='openwrt-18.06.1-x86-64-combined-squashfs.img'
current_release=`awk -F= '/DISTRIB_RELEASE/{print $2}' /etc/openwrt_release | sed "s/\'//g"`
echo $current_release
if echo $update | grep -Fqe $current_release; then
        echo "Is up to date"
else
        reg_server=`cat /etc/register.conf | awk  -F= '/siaddr/{print $2}'`
        `wget http://$reg_server:5000/fw/$update -O /tmp/$update`
        ret=$?
        if [ 0 -eq $ret ]; then
                sysupgrade -v /tmp/$update
        fi
fi
