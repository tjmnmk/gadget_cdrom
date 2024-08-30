#! /bin/bash -eu

if lsmod |grep -q g_mass_storage; then
    rmmod g_mass_storage
fi

if mountpoint -q /iso; then
    umount "$(losetup -PLf /iso.img --show)p1"
fi

if [ ! -f /var/lib/gadget_cdrom_filebrowser.pid ]; then
    exit 0
fi

kill $(cat /var/lib/gadget_cdrom_filebrowser.pid) 2>/dev/null || true
for i in seq 10; do
    if ! ps -p $(cat /var/lib/gadget_cdrom_filebrowser.pid) 2>/dev/null; then
        rm /var/lib/gadget_cdrom_filebrowser.pid
        exit 0
    fi
    sleep 0.01
done

kill -9 $(cat /var/lib/gadget_cdrom_filebrowser.pid) 2>/dev/null || true
rm /var/lib/gadget_cdrom_filebrowser.pid
exit 0