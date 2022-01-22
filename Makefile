INCLUDE = 'yuri,esp8266,pi_pico,uhttpd,esp-series' #要編譯的資料夾

PWD = $(shell pwd)
LOCATE = $(shell pwd)/
FILES = $(shell ./script/list_py_file.py $(PWD) $(LOCATE) $(INCLUDE))
OUTPUTS=$(patsubst %.py, build/mpy/%.mpy, $(FILES))

all:
	@echo "please use 'make esp32' or 'make esp8266'"

build: create_folder $(OUTPUTS) copy_to_dist
	@echo 'Done.'

clean:
	@rm -rf build

create_folder:
	@mkdir -p build/mpy
	@mkdir -p build/dist/lib

copy_to_dist:
	@cp -R build/mpy/yuri build/dist/lib
	@cp -R www build/dist
	@cp -R template build/dist
	@cp build/mpy/esp-series/networkd.mpy build/dist
	@cp build/mpy/esp-series/yhttpd.mpy build/dist
	@cp esp-series/main.py build/dist
	@cp esp-series/boot.py build/dist

esp32: build
	@rm build/dist/lib/yuri/http/handler/fan_control_esp8266.mpy

esp8266: build
	@cp esp-series/main_esp8266.py build/dist/main.py
	@mv build/dist/lib/yuri/http/handler/fan_control_esp8266.mpy build/dist/lib/yuri/http/handler/fan_control.mpy

build/mpy/%.mpy: %.py
	@mkdir -p $(@D)
	mpy-cross -O3 -o $@ $<


