#!/bin/bash -e

install -m 755 /pi-gen/stage-gc/01-sys-tweaks/files/resize2fs_once	"${ROOTFS_DIR}/etc/init.d/"
