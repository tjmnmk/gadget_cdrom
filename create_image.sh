#!/bin/bash -ue

FILE="/iso.img"

if [ -f "$FILE" ] ; then
    echo "$FILE already exists"
    exit 1
fi

free="$(df -h / | tail -n1 | awk '{print $4}')"
echo -ne "Space available: $free\nSize, e.g. 16G? "
read size

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
