CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -g
VALGRIND ?= valgrind
VALGRIND_FLAGS ?= --leak-check=full --error-exitcode=1
BUILD_DIR := build
PROGRAM := $(BUILD_DIR)/duree

.PHONY: all run test memcheck clean

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(PROGRAM): src/main.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

run: $(PROGRAM)
	./$(PROGRAM)

test: $(PROGRAM)
	./$(PROGRAM) | diff -u tests/expected-output.txt -

memcheck: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM)

clean:
	rm -rf $(BUILD_DIR)
