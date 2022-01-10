INCLUDE = 'yuri,esp8266,pi_pico,uhttpd' #要編譯的資料夾

PWD = $(shell pwd)
LOCATE = $(shell pwd)/
FILES = $(shell ./script/list_py_file.py $(PWD) $(LOCATE) $(INCLUDE))
OUTPUTS=$(patsubst %.py, build/mpy/%.mpy, $(FILES))

all: $(OUTPUTS)

clean:
	@rm -rf build

build/mpy/%.mpy: %.py
	@mkdir -p $(@D)
	mpy-cross -O3 -o $@ $<


