#! /bin/bash -eu

IDIR="${BASH_SOURCE%/*}"
if [[ ! -d "$IDIR" ]]; then IDIR="$PWD"; fi

source "$IDIR/clean.sh"

mount -o ro /iso.img /iso
