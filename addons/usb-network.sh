#!/usr/nin/env bash
## Setup base ethernet IP when g_ether is loaded

echo "iface eth0 inet static
    address 10.0.0.1
    netmask 255.255.255.0
    gateway 10.0.0.1" >> /etc/network/interfaces