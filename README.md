# gadget_cdrom
## Requirements
* Requires Raspberry Pi Zero (W) 
* Waveshare 1.3inch OLED HAT (https://www.waveshare.com/wiki/1.3inch_OLED_HAT).
* Raspbian buster

## Description
* gadget_cdrom converts your Raspberry Pi to virtual usb cdrom.
* https://video.ploud.fr/videos/watch/6d0b1014-bb39-4714-a984-15a24a9ac58e

## Usage
* you can switch between HDD mode and virtual cdrom mode.
* HDD mode - in that mode your Raspberry Pi is basically USB flash drive connected to your computer.
* CD mode - in that mode you select some iso you uploaded to Raspberry Pi in HDD mode and after that rpi start pretending it's a cdrom. 

### Keys
* Key1 - Insert iso to the virtual cdrom
* Key2 - Remove iso from virtual cdrom
* Key3 - Change mode
* Joystick Down - next iso
* Joystick Up - previous iso

## Installation
### Install dependecies
```
sudo apt install -y p7zip-full python3-rpi.gpio python3-smbus python3-spidev python3-numpy python3-pil fonts-dejavu ntfs-3g
```

### Prepare storage
```
sudo dd status=progress if=/dev/zero of=/iso.img bs=1M count=24000 #24000 = 24000MB
sudo losetup /dev/loop0 /iso.img
sudo mkfs.ntfs -Q /dev/loop0
sudo losetup -d /dev/loop0
sudo sync
sudo mkdir /iso
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

### Install gadget_cdrom
* Clone gadget_cdrom
```
cd /opt
sudo git clone https://github.com/tjmnmk/gadget_cdrom.git
```
* Enable systemd service:
```
sudo cp /opt/gadget_cdrom/gadget_cdrom.service /etc/systemd/system/gadget_cdrom.service
sudo systemctl enable gadget_cdrom.service
```
* reboot rpi
```
sudo reboot
```
