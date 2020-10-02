#! /bin/bash -eu

IDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$IDIR" ]]; then IDIR="$PWD"; fi

MODE=${1:-hdd}

source "$IDIR/clean.sh"

if [ "$MODE" == "hdd" ] ; then
    if $(lsmod | grep g_ether); then
        rmmod g_ether
    fi
    modprobe g_mass_storage file=/iso.img luns=1 stall=0 ro=0 cdrom=0 removable=1
elif [ "$MODE" == "cd" ] ; then
    mount -o ro "$(losetup -PLf /iso.img --show)p1" /iso
elif [ "$MODE" == "usb" ] ; then
    mount "$(losetup -PLf /iso.img --show)p1" /iso
elif [ "$MODE" == "net" ] ; then
    if $(lsmod | grep g_mass_storage) ; then
        rmmod g_mass_storage
    fi
    modprobe g_ether
fi
