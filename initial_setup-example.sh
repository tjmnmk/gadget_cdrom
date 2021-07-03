#!/usr/bin/env bash
## Setup Raspberry Pi
## You should run walk through this manually while testing. Use at your own risk.

## TODO: Check, so there are no duplicates
## TODO: Set condition for removal of these settings
## TODO: Wifi could be better
## TODO: Capture any error codes
## TODO: Add option to shrink drive


## User options bound to change
wifi_ssid="IP_Daily"
wifi_password="ItHurtsWhenIP"
wifi_country_code="US"

## Options an advanced user may have different preferrences
git_repo="https://github.com/tjmnmk/gadget_cdrom.git"
git_branch="master"
git_directory="gadget_cdrom"
pi_config_txt="/boot/config.txt"
modules="/etc/modules"
wpa_supplicant_dest="/etc/wpa_supplicant/wpa_supplicant.conf"
destination_directory="/opt"

## Add custom boot options
echo "Adding module to $pi_config_txt"
echo "[gadget_cdrom]
dtoverlay=dwc2" >> $pi_config_txt

## Add module to startup
echo "Adding module to $modules"
echo "dwc2" >> $modules

## Add custom options
echo "Updating custom options"
echo "[user_custom]
boot_delay=0
force_turbo=0
disable_splash=1" >> $pi_config_txt

## Enable SPI - reboot needed here
echo "Enabling SPI"
raspi-config nonint do_spi 0

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

## Setup packages
echo "Installing packages"
apt update
apt install -y p7zip-full python3-rpi.gpio python3-smbus python3-spidev \
               python3-numpy python3-pil fonts-dejavu ntfs-3g git

## Adding repo
echo "Setting up repository"
cd $destination_directory
git clone $git_repo $git_directory
cd $git_directory
git pull origin $git_branch
ln -s /opt/$git_directory/gadget_cdrom.service /etc/systemd/system/gadget_cdrom.service
systemctl enable gadget_cdrom.service

## Check if we want to setup the iso image
read -r -p "Would you like to setup the storage where ISOs and USB images will be stored?(y/N)" question
case "$question" in
    [yY][eE][sS]|[yY])
        $destination_directory/$git_directory/create_image.sh || echo "Something went wrong in the storage setup."
    ;;
    * )
        
        exit 0
    ;;
esac

echo "Setup complete, you will want to reboot."

