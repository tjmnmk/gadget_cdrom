#!/bin/bash -ue

auto=0
if [ "$#" -eq 1 ] && [ "$1" = "auto" ]; then
    auto=1
fi

FILE="/iso.img"

if [ -f "$FILE" ]; then
    if [ "$auto" -eq 0 ]; then
        echo "$FILE already exists" 1>&2
        exit 1
    fi
    exit 0
fi

if [ -f "/etc/init.d/resize2fs_once" ] && [ "$auto" -eq 1 ]; then # this is ugly hack :(
    echo "/etc/init.d/resize2fs_once exists" 2>&1
    exit 1
fi

size=0
if [ "$auto" -eq 0 ]; then
    free="$(df -h / | tail -n1 | awk '{print $4}')"
    echo -ne "Space available: $free\nSize, e.g. 16G? "
    read size
else
    free="$(df -k / | tail -n1 | awk '{print $4}')"
    size=$(($free-(1024*1024*2)))
    if [ "$size" -lt "$((free/2))" ]; then
        size=$((free/2))
    fi
    size="${size}k"
fi
 
echo "Creating $size image..."

fallocate -l "$size" "$FILE"
dev="$(losetup -fL --show "$FILE")"
parted "$dev" mklabel msdos
parted "$dev" mkpart p ntfs 1M 100%
mkfs.ntfs -fL RPiHDD "${dev}p1"
losetup -d "$dev"
sync

mkdir -p /iso

echo "Done!"
