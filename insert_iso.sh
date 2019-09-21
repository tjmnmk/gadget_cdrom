#! /bin/bash -eu

iso="$1"

if ! mountpoint -q /iso; then
  exit 1
fi
if ! realpath "/iso/$1" |egrep "^/iso/"; then
  exit 1
fi

modprobe g_mass_storage "file=/iso/$1" luns=1 stall=0 ro=1 cdrom=1 removable=1
