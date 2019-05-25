#!/bin/bash

if [ `whoami` != 'root' ] ; then
	echo "must be root"
	exit
fi

echo Enabling i2c
rcn="$(which raspi-config) nonint"
$rcn do_i2c 0


export DEBIAN_FRONTEND=noninteractive
aptq="apt-get -qq --assume-yes"
apti="$aptq install"

if [[ 0 ]] ; then
  echo Lets update
  $aptq update
  $aptq dist-upgrade
fi

if [[ 0 ]]; then
  echo Lets install some files
  $apti read-edid i2c-tools wiringpi git vim
  $apti libgirepository-1.0 gir1.2-glib
  $apti libavutil-dev libavcodec-dev libavformat-dev libsdl2-dev
  $apti libpython3-dev python3-pip python3-smbus python3-venv python3-gi python3-gi-cairo gir1.2-gtk-3.0
  $apti liblapack3 libclbas3 libatlas3 libatlas3-base libjasper1 openexr libswscale4 libqtgui4 libqt4-test

  $apti gstreamer1.0-tools gstreamer1.0-omx-rpi gstreamer1.0-plugins-{base,good}
fi

usermod -a -G i2c pi
echo dtparam=i2c1_baudrate=1000000 >> /boot/config.txt

pushd ../libs/mlx90640-library/
make I2C_MODE=LINUX

function setup_vkc_python_env() {

pyvenv-3.5 ~/vkc-demo
. ~/vkc-demo/bin/activate

pip install opencv-python Pillow

pushd ../libs/mlx90640-library/python/library/
make
python setup.py install --prefix=~/vkc-demo
deactivate

}

export -f setup_vkc_python_env
su pi -c "bash -c setup_vkc_python_env"

echo REBOOT!!!
