obj-m += st7735fb.o rpi_st7735fb.o

#BUILD_DIR=/lib/module/$(shell uname -r)/build
BUILD_DIR = ~/rpi/kernel/linux

modules:
	make -C $(BUILD_DIR) M=$(PWD) modules

modules_install:
	make -C $(BUILD_DIR) M=$(PWD) modules_install

clean:
	make -C $(BUILD_DIR) M=$(PWD) clean
