#! /bin/bash -eu

if lsmod |grep -q g_mass_storage; then
  rmmod g_mass_storage
fi
