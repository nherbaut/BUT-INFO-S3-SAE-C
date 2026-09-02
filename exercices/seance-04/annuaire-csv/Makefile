CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -g
BUILD_DIR := build
PROGRAM := $(BUILD_DIR)/annuaire-csv
CSV ?= $(BUILD_DIR)/annuaire.csv

.PHONY: all run test clean

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(PROGRAM): src/main.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

run: $(PROGRAM)
	./$(PROGRAM) $(CSV)

test: $(PROGRAM)
	./$(PROGRAM) $(BUILD_DIR)/annuaire-test.csv | diff -u tests/expected-output.txt -

clean:
	rm -rf $(BUILD_DIR)
