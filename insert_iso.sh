#! /bin/bash -eu

iso="$1"
MODE=${2:-cd}

if ! mountpoint -q /iso; then
  exit 1
fi
if ! realpath "$1" |egrep "^/iso/"; then
  exit 1
fi

if [ "$MODE" == "cd" ] ; then
    modprobe g_mass_storage "file=$1" luns=1 stall=0 ro=1 cdrom=1 removable=1
elif [ "$MODE" == "usb" ] ; then
    modprobe g_mass_storage "file=$1" luns=1 stall=0 ro=0 cdrom=0 removable=1
fi
