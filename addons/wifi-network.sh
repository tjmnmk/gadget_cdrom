#!/usr/bin/env bash

## User options bound to change
#wifi_ssid="IP_Daily"
#wifi_password="ItHurtsWhenIP"
wifi_ssid="lofi"
wifi_password="papermachen"
wifi_country_code="US"

## Options an advanced user may have different preferrences
wpa_supplicant_dest="/etc/wpa_supplicant/wpa_supplicant.conf"
destination_directory="/opt"
pi_config_txt="/boot/config.txt"
modules="/etc/modules"

## Add custom options
echo "Updating custom options"
echo "[user_custom]
boot_delay=0
force_turbo=0
disable_splash=1" >> $pi_config_txt

## Setup Wifi
echo "Setting up wifi connection"
echo "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=$wifi_country_code

network={
        ssid=\"$wifi_ssid\"
        psk=\"$wifi_password\"
}" > $wpa_supplicant_dest

systemctl stop wpa_supplicant.service
## It would be nice if services stop when you actually stop them
killall wpa_supplicant
# This is a one time thing and will work properly now and when you reboot
# Tell wpa to run in the background with our new configuration
wpa_supplicant -c /etc/wpa_supplicant/wpa_supplicant.conf -i wlan0 -B
echo "Getting IP from DHCP Server"
## TODO: I am not sure why I get 'too few arguments' here - it still works
dhclient wlan0

## TODO: Add option here to prompt for ethernet (g_ether) IP

## Enable SSH
echo "Enabling SSH"
raspi-config nonint do_ssh 0