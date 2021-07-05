#! /bin/bash -eu

IDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$IDIR" ]]; then IDIR="$PWD"; fi

MODE=${1:-hdd}

source "$IDIR/clean.sh"

if [ "$MODE" == "hdd" ] ; then
    modprobe g_mass_storage file=/dev/mmcblk0p3 luns=1 stall=0 ro=0 cdrom=0 removable=1
elif [ "$MODE" == "cd" ] ; then
    mount -o ro /dev/mmcblk0p3 /iso
elif [ "$MODE" == "usb" ] ; then
    mount  /dev/mmcblk0p3 /iso
elif [ "$MODE" == "net" ] ; then
    modprobe g_ether
elif [ "$MODE" == "shutdown" ]; then
    true
fi
