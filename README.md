# gadget\_cdrom
## Requirements
* Raspberry Pi Zero (2) (W)
* [Waveshare 1.3inch OLED HAT](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)
* Tested on Rasberry Pi OS Buster, Bullseye and [DietPi](https://dietpi.com) Bullseye

## Description
* gadget\_cdrom converts your Raspberry Pi to virtual usb cdrom.
* https://video.ploud.fr/videos/watch/6d0b1014-bb39-4714-a984-15a24a9ac58e
* https://www.youtube.com/watch?v=DntezzK9Eqc

## Usage
* You can switch between HDD mode, virtual cdrom mode, and virtual flash drive mode.
* HDD mode - in that mode your Raspberry Pi is basically USB flash drive connected to your computer.
* CD mode - in that mode you select some iso you uploaded to Raspberry Pi in
  HDD mode, and the rpi will pretend to be that cdrom.
* USB mode - the rpi will pretend to be a flash drive, presenting the usb .img
  you selected.

### Keys
* Key1 - Activate selected image
* Key2 - Deactivate image
* Key3 - Change mode
* Joystick Down - next image
* Joystick Up - previous image
* Joystick Left - shutdown / power on

## RPI Images
### DietPi + gadget_cdrom image
There are customized DietPi images with gadget_cdrom and kernel patch for big isos in the [releases section](https://github.com/tjmnmk/gadget_cdrom/releases), just write it to sd-card (you can use rpi-imager, dd, etc.), turn rpi on and wait a few minutes to get everything ready.

### Banana Pi M2 Zero Image
https://github.com/rzrbld/gadget_cdrom_bpi_m2_zero

## Manual Installation
### Install dependencies
```
sudo apt install -y p7zip-full python3-rpi.gpio python3-smbus python3-spidev \
                    python3-numpy python3-pil fonts-dejavu ntfs-3g
```

### Prepare storage
```sh
# sudo ./create_image.sh
Space available: 24G
Size, e.g. 16G? 8G"
Creating 8G image...
Done!
```

### Load modules after boot
* Add ```dtoverlay=dwc2``` to /boot/config.txt
* Add ```dwc2``` to /etc/modules
* Enable SPI
```
sudo raspi-config
Interfacing Options
SPI
Yes
```

### Install gadget\_cdrom
* Clone gadget_cdrom
```
cd /opt
sudo git clone https://github.com/tjmnmk/gadget_cdrom.git
```
* Enable systemd service:
```
sudo ln -s /opt/gadget_cdrom/gadget_cdrom.service /etc/systemd/system/gadget_cdrom.service
sudo systemctl enable gadget_cdrom.service
```
* reboot rpi
```
sudo reboot
```

### Optional
#### Recompile kernel for support isos bigger than ~2.5GB
* Apply this [patch](../master/tools/kernel/00-remove_iso_limit.patch)
* Build kernel: https://www.raspberrypi.org/documentation/linux/kernel/building.md
