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
PROGRAM := $(BUILD_DIR)/stats
OBJS := $(BUILD_DIR)/main.o $(BUILD_DIR)/stats.o

.PHONY: all test memcheck memcheck-tests memcheck-run memcheck-scenario clean run

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/main.o: src/main.c include/projet/stats.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/stats.o: src/stats.c include/projet/stats.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(PROGRAM): $(OBJS) | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $^ $(LDLIBS) -o $@

run: $(PROGRAM)
	./$(PROGRAM)

test: $(PROGRAM)
	./$(PROGRAM) | grep -q "moyenne = 12.00"

memcheck: memcheck-tests

memcheck-tests: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM)

memcheck-run: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(ARGS)

memcheck-scenario: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(SCENARIO_ARGS)

clean:
	rm -rf $(BUILD_DIR)
