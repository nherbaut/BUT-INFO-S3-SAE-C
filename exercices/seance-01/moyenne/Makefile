CC ?= cc
CPPFLAGS ?= -Iinclude
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic
LDFLAGS ?=
LDLIBS ?=

VALGRIND ?= valgrind
VALGRIND_FLAGS ?= \
	--leak-check=full \
	--show-leak-kinds=all \
	--errors-for-leak-kinds=definite,indirect,possible \
	--track-origins=yes \
	--error-exitcode=1

ARGS ?=
SCENARIO_ARGS ?=

BUILD_DIR := build
PROGRAM := $(BUILD_DIR)/moyenne

.PHONY: all test memcheck memcheck-tests memcheck-run memcheck-scenario clean run

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(PROGRAM): src/main.c | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $< $(LDLIBS) -o $@

run: $(PROGRAM)
	printf "12 14\n" | ./$(PROGRAM)

test: $(PROGRAM)
	printf "12 14\n" | ./$(PROGRAM) | grep -q "moyenne = 13"

memcheck: memcheck-tests

memcheck-tests: $(PROGRAM)
	printf "12 14\n" | $(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM)

memcheck-run: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(ARGS)

memcheck-scenario: $(PROGRAM)
	printf "12 14\n" | $(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(SCENARIO_ARGS)

clean:
	rm -rf $(BUILD_DIR)
