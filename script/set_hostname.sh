#!/bin/sh
uci set system.@system[0].hostname=$1
uci commit system
/etc/init.d/system reload

