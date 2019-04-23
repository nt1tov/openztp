#!/bin/sh
update=$1
current_release=`awk -F= '/DISTRIB_RELEASE/{print $2}' /etc/openwrt_release | sed "s/\'//g"`
echo $current_release
if echo $update | grep -Fqe $current_release; then
        echo "Is up to date"
else
        `wget -q http://192.168.56.1:5000/fw/$update -O /tmp/$update`
        ret=$?
        if [ 0 -eq $ret ]; then
                sysupgrade -v /tmp/$update
        fi
fi

