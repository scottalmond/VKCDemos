#!/bin/bash

. common.sh

checkroot
doing_updates

echo Enabling Camera
$rcn do_camera 0

if [[ $do_installs == true ]]; then
  echo Lets install some files
  $apti read-edid i2c-tools wiringpi git vim
  $apti libgirepository-1.0 gir1.2-glib
  $apti libavutil-dev libavcodec-dev libavformat-dev libsdl2-dev
  $apti libpython3-dev python3-pip python3-smbus python3-venv python3-gi python3-gi-cairo gir1.2-gtk-3.0
  $apti liblapack3 libclbas3 libatlas3 libatlas3-base libjasper1 openexr libswscale4 libqtgui4 libqt4-test
  $apti python-gi python3-gi \
    gstreamer1.0-tools \
    gir1.2-gstreamer-1.0 \
    gir1.2-gst-plugins-base-1.0 \
    gstreamer1.0-libav
  $apti gstreamer1.0-tools gstreamer1.0-omx-rpi gstreamer1.0-plugins-{base,good,ugly,bad}
  $apti gstreamer1.0-omx-rpi-config gstreamer1.0-omx

  $apti uvcdynctrl
fi

if ! grep -q bcm2835-v4l2 /etc/modules ; then
    echo bcm2835-v4l2 >> /etc/modules
fi

function setup_vkc_python_env() {
if [ ! -d ${pyvenv_dir} ] ; then
	echo creating environment
    pyvenv-3.5 --system-site-packages ${pyvenv_dir}
fi

. ${pyvenv_dir}/bin/activate

pip install opencv-python Pillow "picamera[array]"

deactivate

}

export -f setup_vkc_python_env
su pi -c "bash -c setup_vkc_python_env"

echo REBOOT!!!
# vim: set ts=4 sw=4 tw=0 noet: expandtab:
