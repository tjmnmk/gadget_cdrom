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
ln -s /opt/gadget_cdrom/gadget_cdrom_auto_img.service /etc/systemd/system/gadget_cdrom.service
systemctl enable gadget_cdrom.service
EOF

echo >> "${ROOTFS_DIR}/etc/modules"
echo dwc2 >> "${ROOTFS_DIR}/etc/modules"

set_config_txt "dtoverlay" "dwc2"
set_config_txt "dtparam=spi" "on"



