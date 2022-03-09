INCLUDE = 'yuri,esp8266,pi_pico,uhttpd,esp-series' #要編譯的資料夾

PWD = $(shell pwd)
LOCATE = $(shell pwd)/
FILES = $(shell ./script/list_py_file.py $(PWD) $(LOCATE) $(INCLUDE))
OUTPUTS=$(patsubst %.py, build/mpy/%.mpy, $(FILES))

all: clean_dist create_folder $(OUTPUTS) copy_to_dist
	@echo 'Done.'

clean:
	@rm -rf build

clean_dist:
	@rm -rf build/dist

create_folder:
	@mkdir -p build/mpy
	@mkdir -p build/dist/esp32/lib/yuri
	@mkdir -p build/dist/esp8266/lib/yuri
	@mkdir -p build/dist/pico/lib/yuri

copy_to_dist:
	@#esp32
	@cp -R build/mpy/yuri build/dist/esp32/lib
	@cp -R www build/dist/esp32
	@cp -R template build/dist/esp32
	@cp build/mpy/esp-series/networkd.mpy build/dist/esp32
	@cp build/mpy/esp-series/yhttpd.mpy build/dist/esp32
	@cp esp-series/main.py build/dist/esp32
	@cp esp-series/boot.py build/dist/esp32
	@rm build/dist/esp32/lib/yuri/http/handler/fan_control_esp8266.mpy
	@rm build/dist/esp32/lib/yuri/uart_reader.mpy

	@#pico
	@cp build/mpy/yuri/uart_reader.mpy build/dist/pico/lib/yuri/
	@cp build/mpy/yuri/stream* build/dist/pico/lib/yuri/

	@#esp8266
	@cp -R build/mpy/yuri build/dist/esp8266/lib
	@cp -R www build/dist/esp8266
	@cp -R template build/dist/esp8266
	@cp build/mpy/esp-series/networkd.mpy build/dist/esp8266
	@cp build/mpy/esp-series/yhttpd.mpy build/dist/esp8266
	@cp esp-series/main_esp8266.py build/dist/esp8266/main.py
	@cp esp-series/boot.py build/dist/esp8266
	@mv build/dist/esp8266/lib/yuri/http/handler/fan_control_esp8266.mpy build/dist/esp8266/lib/yuri/http/handler/fan_contro.mpy
	@rm build/dist/esp8266/lib/yuri/uart_reader.mpy

build/mpy/%.mpy: %.py
	@mkdir -p $(@D)
	mpy-cross -O3 -o $@ $<

src:
	#
	@mkdir -p build/src
	@rm -rf build/src

	@mkdir -p build/src/esp32/lib/yuri
	@mkdir -p build/src/esp8266/lib/yuri
	@mkdir -p build/src/pico/lib/yuri

	@#esp32
	@cp -R yuri build/src/esp32/lib/
	@cp -R www build/src/esp32
	@cp -R template build/src/esp32
	@cp esp-series/networkd.py build/src/esp32
	@cp esp-series/yhttpd.py build/src/esp32
	@cp esp-series/main.py build/src/esp32
	@cp esp-series/boot.py build/src/esp32
	@rm build/src/esp32/lib/yuri/http/handler/fan_control_esp8266.py
	@rm build/src/esp32/lib/yuri/uart_reader.py

	@#esp8266
	@cp -R yuri build/src/esp8266/lib
	@cp -R www build/src/esp8266
	@cp -R template build/src/esp8266
	@cp esp-series/networkd.py build/src/esp8266
	@cp esp-series/yhttpd.py build/src/esp8266
	@cp esp-series/main_esp8266.py build/src/esp8266/main.py
	@cp esp-series/boot.py build/src/esp8266
	@mv build/src/esp8266/lib/yuri/http/handler/fan_control_esp8266.py build/src/esp8266/lib/yuri/http/handler/fan_contro.py
	@rm build/src/esp8266/lib/yuri/uart_reader.py

	@#pico
	@cp yuri/uart_reader.py build/src/pico/lib/yuri/
	@cp yuri/stream* build/src/pico/lib/yuri/


