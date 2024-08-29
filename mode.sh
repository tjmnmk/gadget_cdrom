#! /bin/bash -eu

IDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$IDIR" ]]; then IDIR="$PWD"; fi

MODE=${1:-hdd}
FILEBROWSER=${2:-true}

source "$IDIR/clean.sh"

if [ "$MODE" == "hdd" ] ; then
    modprobe g_mass_storage file=/iso.img luns=1 stall=0 ro=0 cdrom=0 removable=1
elif [ "$MODE" == "cd" ] ; then
    mount -o ro "$(losetup -PLf /iso.img --show)p1" /iso
elif [ "$MODE" == "usb" ]; then
    mount "$(losetup -PLf /iso.img --show)p1" /iso
elif [ "$MODE" == "upload" ]; then
    mount "$(losetup -PLf /iso.img --show)p1" /iso
    $FILEBROWSER &
    # save pid
    echo "$!" > /var/lib/gadget_cdrom_filebrowser.pid
elif [ "$MODE" == "shutdown" ]; then
    true
fi
