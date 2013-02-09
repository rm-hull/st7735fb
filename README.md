ST7735 FrameBuffer for Raspberry Pi
===================================

The ST7735 is a single-chip controller/driver for 262K-color, graphic type 
TFT-LCD, which can be picked up on eBay relatively cheaply with pin-outs on
a break-out board.

![1.8" 160x128 pixel TFT-LCD](http://www.adafruit.com/adablog/wp-content/uploads/2011/12/window-57.jpg)

Originally based on code from https://github.com/ohporter/linux-am33x/tree/st7735fb

Further technical details for the LCD screen can be found in the 
[datasheet](https://raw.github.com/rm-hull/st7735-fb/master/doc/tech-spec/datasheet.pdf) [PDF]. Tested working
with Rev B 512Mb Rasberry Pi (Raspbian "Wheezy" & latest [RPi-Firmware](https://github.com/Hexxeh/rpi-update))

Pre-requisites
--------------
- to do

1. Enable SPI by editing `/etc/modprobe.d/raspi-blacklist.conf` to comment out blacklisting of _spi_bcm2708_.

2. Ensure the gcc build tools are installed: 

    $ sudo apt-get install build-essential

Building and installing the frame buffer driver
-----------------------------------------------
- to do

Once compiled, installed and inserted, you should get a second frame buffer at `/dev/fb1`.

Pin-outs
--------
There appear to be a large number of break-out boards for this device; this one works for me:

| Pin | Name    | Description              |
|----:|:--------|:-------------------------|
| 1   | GND     | 0V                       |
| 2   | VCC     | 3V3                      |
| 3   | NC      |                          |
| 4   | NC      |                          |
| 5   | NC      |                          |
| 6   | RESET   | Set low to reset         |
| 6   | A0      | SPI data/command         |
| 7   | SDA     | SPI data                 |
| 8   | SCK     | SPI clock                |
| 9   | CS      | Chip select - set low    |
| 10  | SD-SCK  | SD serial clock          |
| 11  | SD-MISO | SD master in, slave out  |
| 12  | SD-MOSI | SD master out, slave in  |
| 13  | SD-CS   | SD chip select           |
| 14  | LED+    |   aligned                |
| 15  | LED-    |   aligned                |

Wiring Schematic
----------------
- to do

Stripboard Layout
-----------------
- to do

Testing
-------
## mplayer
WIDTH is the display width.  
_scale_ is used because the movie is larger than most small displays. -3 means keep aspect ratio and calculate height.

    $ apt-get install -y mplayer
    $ wget http://fredrik.hubbe.net/plugger/test.mpg

    $ mplayer -nolirc -vo fbdev2:/dev/fb1 -vf scale=WIDTH:-3 test.mpg

## Image viewer

    $ apt-get -y install fim
    $ wget http://www.olsug.org/wiki/images/9/95/Tux-small.png

    $ FRAMEBUFFER=/dev/fb1 fim Tux-small.png

## Console
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

