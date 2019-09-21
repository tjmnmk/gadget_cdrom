#! /bin/bash -eu

if ! mountpoint -q /iso; then
  exit 1
fi

find /iso -type f -iname "*.iso" -printf "%f\n"