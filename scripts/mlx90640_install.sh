#!/bin/bash

. common.sh

: ${use_whl:=true}
export use_whl

checkroot
doing_updates

echo Enabling i2c
$rcn do_i2c 0

if [[ $do_installs == true ]]; then
  echo Lets install some files
  pkgs=(read-edid i2c-tools wiringpi git vim)
  pkgs=(libgirepository-1.0 gir1.2-glib)
  pkgs=(libavutil-dev libavcodec-dev libavformat-dev libsdl2-dev)
  pkgs=(libpython3-dev python3-pip python3-smbus python3-venv python3-gi python3-gi-cairo gir1.2-gtk-3.0)
  pkgs=(liblapack3 libatlas-base-dev libatlas3-base libjasper1 openexr libswscale4 libqtgui4 libqt4-test)
  pkgs=(python-gi python3-gi \
    gstreamer1.0-tools \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-libav)
      pkgs=(gstreamer1.0-tools gstreamer1.0-omx-rpi gstreamer1.0-plugins-{base,good,ugly,bad})
  pkgs=(gstreamer1.0-omx-rpi-config gstreamer1.0-omx)

  pkgs=(libi2c-dev swig3.0 tcl8.6-dev)

  $apti ${pkgs[@]}
fi

usermod -a -G i2c pi
if ! grep -q "dtparam=i2c1_baudrate=1000000"   /boot/config.txt ; then
    echo      dtparam=i2c1_baudrate=1000000 >> /boot/config.txt
fi

#pushd ${VKCDemos_src}/libs/mlx90640-library
#sed 's/bcm2835-1.55/bcm2835-1.60/g' Makefile -i
#make bcm2835
#make I2C_MODE=LINUX libMLX90640_API.so
#popd

function setup_vkc_python_env() {
if [ ! -d ${pyvenv_dir} ] ; then
	echo creating environment
    python3 -m venv --system-site-packages ${pyvenv_dir}
fi

. ${pyvenv_dir}/bin/activate

python -m pip install --user pip
#python -m pip install opencv-python
python -m pip install Pillow

if [[ ${use_whl} == true ]] ; then
  python -m pip install ${VKCDemos_src}/scripts/python-pkgs/MLX90640-0.0.2-cp37-cp37m-linux_armv7l.whl
else
  pushd ${VKCDemos_src}/libs/mlx90640-library/python/library/
  make
  python setup.py install --prefix=${pyvenv_dir}
  popd
fi

deactivate

}

export -f setup_vkc_python_env
su pi -c "bash -c setup_vkc_python_env"

echo REBOOT!!!
# vim: set ts=4 sw=4 tw=0 noet: expandtab:
