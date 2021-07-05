#!/usr/bin/env bash
## Setup Raspberry Pi
## You should run walk through this manually while testing. Use at your own risk.

## TODO: Check, so there are no duplicates
## TODO: Capture any error codes
## TODO: Add option to shrink drive

## Options an advanced user may have different preferrences
#git_repo="https://github.com/tjmnmk/gadget_cdrom.git"
#git_branch="master"
git_repo="https://github.com/lordbink/gadget_cdrom.git"
git_branch="master"
git_directory="gadget_cdrom"
pi_config_txt="/boot/config.txt"
modules="/etc/modules"
destination_directory="/opt"

## Add custom boot options
echo "Adding module to $pi_config_txt"
echo "[gadget_cdrom]
dtoverlay=dwc2" >> $pi_config_txt

## Add module to startup
echo "Adding module to $modules"
echo "dwc2" >> $modules

## Enable SPI - reboot needed here
echo "Enabling SPI"
raspi-config nonint do_spi 0

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

