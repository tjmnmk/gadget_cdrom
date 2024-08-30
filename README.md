# gadget\_cdrom

## Requirements

* Raspberry Pi Zero (2) (W) or Raspberry Pi 4 (Not tested!)
* [Waveshare 1.3inch OLED HAT](https://www.waveshare.com/wiki/1.3inch_OLED_HAT)
* Tested on Rasberry Pi OS Buster, Bullseye and [DietPi](https://dietpi.com) Bullseye

## Description

* gadget\_cdrom converts your Raspberry Pi to virtual usb cdrom.
* <https://www.youtube.com/watch?v=DntezzK9Eqc>

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

<https://github.com/rzrbld/gadget_cdrom_bpi_m2_zero>

## Manual Installation

### Install dependencies

```sh
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

```sh
sudo raspi-config
Interfacing Options
SPI
Yes
```

### Install gadget\_cdrom

* Clone gadget_cdrom

```sh
cd /opt
sudo git clone https://github.com/tjmnmk/gadget_cdrom.git
```sh
* Enable systemd service:
```sh
sudo ln -s /opt/gadget_cdrom/gadget_cdrom.service /etc/systemd/system/gadget_cdrom.service
sudo systemctl enable gadget_cdrom.service
```sh
* reboot rpi
```sh
sudo reboot
```

### Optional

#### Recompile kernel for support isos bigger than ~2.5GB

* Apply this [patch](../master/tools/kernel/00-remove_iso_limit.patch)
* Build kernel: https://www.raspberrypi.org/documentation/linux/kernel/building.md

### Install Filebrowser and Enable Upload Mode

To enable the upload mode, you need to install [Filebrowser](https://filebrowser.org/) and configure it in the `config.yaml` file.

* **Install Filebrowser:**

   ```sh
   curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash
   ```

* **Enable Upload Mode:**
  Set value of `WEB_INTERFACE_ENABLED` in `config.yaml` to `true`.

## Configuration

The `config.yaml` file contains the following configuration options:

* `WEB_INTERFACE_ENABLED`: Enable the web interface (true/false).
* `WEB_INTERFACE_PORT`: The port on which the web interface will be available.
* `WEB_INTERFACE_HOST`: The host for the web interface.

* `UPLOAD_MODE_ENABLED`: Enable upload mode (true/false) - you need to have a [filebrowser](https://filebrowser.org/) installed.
* `UPLOAD_MODE_DISPLAY_TOOGLE`: Display the upload mode toggle (true/false).
* `FILEBROWSER_BIN`: Command to launch the [filebrowser](https://filebrowser.org/).
* `FILEBROWSER_URL`: URL address of the [filebrowser](https://filebrowser.org/).

* `INFO_MODE_ENABLED`: Enable info mode (true/false).
* `INFO_MESSAGE`: Messages displayed in info mode.

* `FONT`: Path to the font file.

Example configuration:

```yaml
WEB_INTERFACE_ENABLED: false
WEB_INTERFACE_PORT: 9000
WEB_INTERFACE_HOST: "::"

UPLOAD_MODE_ENABLED: false
UPLOAD_MODE_DISPLAY_TOOGLE: false
FILEBROWSER_BIN: "filebrowser -a [::] -r /iso -p 9001 --disable-exec --noauth"
FILEBROWSER_URL: "http://localhost:9001"

INFO_MODE_ENABLED: false
INFO_MESSAGE: [ "gadget_cdrom v1.1.0", "http://192.168.0.1:9000/", "SSID: gadgetcdrom" ]

FONT: "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
```
