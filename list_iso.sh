#! /bin/bash -eu

if ! mountpoint -q /iso; then
    exit 1
fi

EXT=${1:-iso}

find /iso -type f -iname "*.$EXT" -not -path '*/.*' -print0
