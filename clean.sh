#! /bin/bash -eu

## Not a garuntee this will prevent issues if copying files while chaging modes
## but should help
sync

if lsmod |grep -q g_mass_storage; then
    rmmod g_mass_storage
fi

if lsmod |grep -q g_ether; then
    rmmod g_ether
fi

if mountpoint -q /iso; then
    umount "$(losetup -PLf /iso.img --show)p1"
fi
