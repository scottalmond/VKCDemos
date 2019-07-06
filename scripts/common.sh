#!/bin/bash

: ${do_updates:=false}
: ${do_installs:=true}

export do_updates
export do_installs

: ${VKCDemos_src:=/home/pi/src/VKCDemos}
: ${pyvenv_dir:=/home/pi/vkc-demo}

export VKCDemos_src
export pyvenv_dir

: ${apt_qq:=false}

export apt_qq

function checkroot() {
    if [ `whoami` != 'root' ] ; then
        echo "must be root"
        exit
    fi
}

export rcn="$(which raspi-config) nonint"

if [[ ${apt_qq} ]] ; then
    export aptq="apt-get -qq --assume-yes"
else
    export aptq="apt-get --assume-yes"
fi


export DEBIAN_FRONTEND=noninteractive
export apti="$aptq install"

function doing_updates() {
	echo do_updates is ${do_updates}
	if [[ $do_updates == true ]] ; then
		echo Lets update
		$aptq update
		$aptq dist-upgrade
		do_updates=false
	fi
}

# vim: set ts=4 sw=4 tw=0 noet: expandtab:
