#!/bin/bash -eu

function set_config_txt {
    local key="$1"
    local value="$2"

    if egrep -q "^${key}=" "${ROOTFS_DIR}/boot/config.txt"; then
        sed "s/${key}=.*/${key}=${value}/g" -i "${ROOTFS_DIR}/boot/config.txt"
    else
        echo >> "${ROOTFS_DIR}/boot/config.txt"
        echo "${key}=${value}" >> "${ROOTFS_DIR}/boot/config.txt"
    fi
}

cd "${ROOTFS_DIR}/opt"
git clone https://github.com/tjmnmk/gadget_cdrom.git

on_chroot << EOF
systemctl enable /opt/gadget_cdrom/gadget_cdrom_auto_img.service
EOF

echo >> "${ROOTFS_DIR}/etc/modules"
echo dwc2 >> "${ROOTFS_DIR}/etc/modules"

vmlinuz_fname=$(dpkg -c /pi-gen/stage-gc/00-gadget_cdrom/files/kernel_packages/linux-image-*_armhf.deb |grep ./boot/vmlinuz |awk -F"/" '{print $NF}')
for i in /pi-gen/stage-gc/00-gadget_cdrom/files/kernel_packages/linux*.deb; do
       install -m 644 "$i" "${ROOTFS_DIR}/root/"
done
install -m 755 "/pi-gen/stage-gc/00-gadget_cdrom/files/config.txt" "/boot/"
on_chroot << EOF
dpkg -i /root/linux*.deb
EOF
 
set_config_txt "kernel" "$vmlinuz_fname"
