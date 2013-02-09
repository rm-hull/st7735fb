ST7735 FrameBuffer for Raspberry Pi
===================================

The ST7735 is a single-chip controller/driver for 262K-color, graphic type 
TFT-LCD, which can be picked up on eBay relatively cheaply with pin-outs on
a break-out board.

![1.8" 160x128 pixel TFT-LCD](http://www.adafruit.com/adablog/wp-content/uploads/2011/12/window-57.jpg)

Originally based on code from https://github.com/ohporter/linux-am33x/tree/st7735fb. 
Tested working with Rev B 512Mb Rasberry Pi (Raspbian "Wheezy" & latest [RPi-Firmware](https://github.com/Hexxeh/rpi-update), 
kernel 3.6.11+ #371)

Further technical details for the LCD screen can be found in the 
[datasheet](https://raw.github.com/rm-hull/st7735-fb/master/doc/tech-spec/datasheet.pdf) [PDF]. Other documentation
can also be found in `docs/tech-spec`.

Pre-requisites
--------------
1. On the Raspberry Pi, enable SPI: edit `/etc/modprobe.d/raspi-blacklist.conf`
   to comment out blacklisting of _spi_bcm2708_.

2. Ensure that the latest firmware has been applied to the Raspberry Pi. Use the updater from
   https://github.com/Hexxeh/rpi-update to perform the update. After rebooting, confirm the
   kernel version as follows:

      ```
      $ uname -a
      Linux raspberrypi 3.6.11+ #371 PREEMPT Thu Feb 7 16:31:35 GMT 2013 armv6l GNU/Linux
      ```

3. Ensure the gcc build tools are installed on a host PC (it is much
   quicker to cross-compile than build the kernel on the RPi): 

      ```
      $ sudo apt-get install build-essential ncurses-dev
      ```

4. Follow the instructions for building a cross-compiled kernel [here](http://elinux.org/RPi_Kernel_Compilation).
   Note that: 
   * it is only necessary to compile the kernel (up-to section 4 'Perform the compilation' in the guide).
   * when the guide refers to `.config`, this is provided as `etc/config.gz` in git.

Building and installing the frame buffer driver
-----------------------------------------------
Once compiled, installed and inserted, you should get a second frame buffer at `/dev/fb1`.

Pin-outs
--------
There appear to be a large number of break-out boards available for this device; this is the one 
I have, with an additional SD card slot:

| TFT Pin | Name    | Remarks                     | RPi Pin | RPi Function      |
|--------:|:--------|:----------------------------|--------:|-------------------|
| 1       | GND     | Ground                      | 6       | GND               |
| 2       | VCC     | Power                       | 1       | 3V3)              |
| 3       | NC      |                             |         |                   |
| 4       | NC      |                             |         |                   |
| 5       | NC      |                             |         |                   |
| 6       | RESET   | Set low to reset            | 18      | GPIO 24           |
| 7       | A0      | Data/command select (_aka_ 'register select')        | 16      | GPIO 23           |
| 8       | SDA     | SPI data                    | 19      | GPIO 10 (MOSI)    |
| 9       | SCK     | SPI clock                   | 23      | GPIO 11 (SPI CLK) |
| 10      | CS      | SPI chip select - set low   | 24      | GPIO 8 (SPI CS0)  |
| 11      | SD-SCK  | SD serial clock             |         |                   |
| 12      | SD-MISO | SD master in, slave out     |         |                   |
| 13      | SD-MOSI | SD master out, slave in     |         |                   |
| 14      | SD-CS   | SD chip select              |         |                   |
| 15      | LED+    | Backlight control 3V3 - 3V7, already fitted with 10R resistor? | 12      | GPIO 18 (PWM CLK) |
| 16      | LED-    | Backlight ground            | 6       | GND               |

Wiring Schematic
----------------
- to do

Stripboard Layout
-----------------
- to do

Testing
-------
### mplayer
WIDTH is the display width. _scale_ is used because the movie is larger than most small displays. -3 means keep aspect ratio and calculate height.

    $ mplayer -nolirc -vo fbdev2:/dev/fb1 -vf scale=WIDTH:-3 examples/test.mpg

### Image viewer

    $ FRAMEBUFFER=/dev/fb1 fim examples/Tux-small.png

### Console
Use display as the primary console.  
If a keyboard is plugged in after power on, a reboot may be necessary.

Map console 1 to framebuffer 1, login screen will show up on the display

    $ con2fbmap 1 1

    $ con2fbmap 1
    console 1 is mapped to framebuffer 1

Revert

    $ con2fbmap 1 0

Using the LCD as a console device
---------------------------------
To use the display as a console, add this to the end of the line in `/boot/cmdline.txt`

    fbcon=map:10 fbcon=font:ProFont6x11

*fbcon=rotate:1* can also be used. See
[fbcon doc](http://www.mjmwired.net/kernel/Documentation/fb/fbcon.txt#72)
for more info.

TODO
----
* Extended documentation

* Improve build instructions

* Schematics & stripboard wiring

* Example code (SDL / Python)

References
----------
* http://www.sitronix.com.tw/sitronix/product.nsf/Doc/ST7735?OpenDocument

* http://learn.adafruit.com/1-8-tft-display

* http://www.raspberrypi.org/phpBB3/viewtopic.php?t=28696&p=262909

* http://elinux.org/images/1/19/Passing_Time_With_SPI_Framebuffer_Driver.pdf

* http://www.flickr.com/photos/ngreatorex/7672743302/

* https://github.com/notro/fbtft

* http://fritzing.org

