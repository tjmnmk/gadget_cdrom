#! /bin/bash -eu
#modprobe binfmt_misc
git clone https://github.com/RPi-Distro/pi-gen.git
rsync -av config pi-gen/
rsync -av stage-gc pi-gen/
cd pi-gen
PRESERVE_CONTAINER=1 ./build-docker.sh
