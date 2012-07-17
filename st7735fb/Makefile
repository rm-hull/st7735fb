obj-m += st7735fb.o

modules:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

modules_install:
	make -C /lib/modules/${shell uname -r}/build M=${PWD} modules_install

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
