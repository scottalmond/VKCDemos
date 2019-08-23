#!/bin/bash

mcwd="$(dirname "$(readlink -f "$0")")"
source $mcwd/common.sh

checkroot
doing_updates

echo Enabling Camera
$rcn do_camera 0

if [[ $do_installs == true ]]; then
  echo Lets install some files
  pkgs=(git vim)
  pkgs+=(read-edid i2c-tools wiringpi)
  pkgs+=(libgirepository-1.0 gir1.2-glib)
  pkgs+=(libavutil-dev libavcodec-dev libavformat-dev libsdl2-dev)
  pkgs+=(libpython3-dev python3-pip python3-smbus python3-venv python3-gi python3-gi-cairo gir1.2-gtk-3.0)
  pkgs+=(liblapack3 libatlas-base-dev libatlas3-base libjasper1 openexr libswscale{5,-dev} libqtgui4 libqt4-test)
  pkgs+=(python-gi python3-gi \
    gstreamer1.0-tools \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-libav)
  pkgs+=(gstreamer1.0-tools gstreamer1.0-omx-rpi gstreamer1.0-plugins-{base,good,ugly,bad})
  pkgs+=(gstreamer1.0-omx-rpi-config gstreamer1.0-omx)

  pkgs+=(uvcdynctrl)
  pkgs+=(python3-opencv)

  $apti ${pkgs[@]}
fi

usermod -a -G video pi
if ! grep -q bcm2835-v4l2 /etc/modules ; then
    echo bcm2835-v4l2 >> /etc/modules
fi

function setup_vkc_python_env() {
if [ ! -d ${pyvenv_dir} ] ; then
	echo creating environment
    python3 -m venv --system-site-packages ${pyvenv_dir}
fi

. ${pyvenv_dir}/bin/activate

python -m pip install --user pip
#python -m pip install opencv-python
python -m pip install Pillow "picamera[array]"

deactivate

}

export -f setup_vkc_python_env
su pi -c "bash -c setup_vkc_python_env"

echo REBOOT!!!
# vim: set ts=4 sw=4 tw=0 noet: expandtab:
