#! /bin/bash -eu

IDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$IDIR" ]]; then IDIR="$PWD"; fi

source "$IDIR/clean.sh"

modprobe g_mass_storage file=/iso.img luns=1 stall=0 ro=0 cdrom=0 removable=1

