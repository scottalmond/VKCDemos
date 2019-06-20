# Software
Software is installed on the Raspberry Pi. Fetch the image and install according from [raspberrypi.org][rpi-rasp-dl]. This demo is using the "Raspbian Stretch with desktop" Image. Once installed, login to the Raspberry Pi and then fetch the source

~~~
mkdir src
cd src
git clone https://github.com/scottalmond/VKCDemos.git
cd VKCDemos
git submodule update --init --recursive
~~~

# VKCDemos

## MLX90640
This is an overview of installing and using the [MLX90640][mlx90640-ref]. This example uses [this][mlx90640-lib] Library.

### Hook-up

#### Wires for I2C 
[<img src="docs/MLX90640_and_RPi.png" width=300>][mlx90640-hookup]

#### Install MLX90640 Software

There is a install script that should (currently)

 * Install the dependancies
 * Setup I2C
 * Build the library and install the python library
 * Setup a [python virtual environment][py-venv] in `~/vkc-demo`

Run the install script by:
~~~
cd scripts
sudo mlx90640_install.sh
~~~
Finally, reboot.

### Usage

~~~
cd src/drivers/peripherals/
sudo ./mlx906640.sh
~~~

[rpi-rasp-dl]:     https://www.raspberrypi.org/downloads/raspbian/
[mlx90640-ref]:    https://www.sparkfun.com/products/14844
[mlx90640-lib]:    https://github.com/pimoroni/mlx90640-library
[mlx90640-hookup]: https://learn.sparkfun.com/tutorials/qwiic-ir-array-mlx90640-hookup-guide/all
[py-venv]:         https://docs.python.org/3/library/venv.html


