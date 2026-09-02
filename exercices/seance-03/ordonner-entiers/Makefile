CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -g
BUILD_DIR := build
PROGRAM := $(BUILD_DIR)/ordonner-entiers

.PHONY: all run test clean

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(PROGRAM): src/main.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

run: $(PROGRAM)
	./$(PROGRAM)

test: $(PROGRAM)
	./$(PROGRAM) | diff -u tests/expected-output.txt -

clean:
	rm -rf $(BUILD_DIR)
