#! /bin/bash -eu

if ! mountpoint -q /iso; then
  exit 1
fi

find /iso -maxdepth 1 -type f -iname "*.iso" -printf "%f\n"