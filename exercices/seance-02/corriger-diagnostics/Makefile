CFLAGS = -Iinclude -std=c11 -Wall -Wextra -Wpedantic -Wconversion -Werror -O2 -g

.PHONY: all run test clean

all: build/diagnostics

build/main.o: src/main.c include/projet/report.h
	mkdir -p build
	cc $(CFLAGS) -c src/main.c -o build/main.o

build/report.o: src/report.c include/projet/report.h
	mkdir -p build
	cc $(CFLAGS) -c src/report.c -o build/report.o

build/diagnostics: build/main.o build/report.o
	cc $(CFLAGS) build/main.o build/report.o -o build/diagnostics

run: build/diagnostics
	./build/diagnostics

test: build/diagnostics
	printf "9\\n" | ./build/diagnostics | diff -u tests/expected-output.txt -

clean:
	rm -rf build
