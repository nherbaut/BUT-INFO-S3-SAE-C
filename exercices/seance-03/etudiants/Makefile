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
PROGRAM := $(BUILD_DIR)/etudiants
OBJS := $(BUILD_DIR)/main.o $(BUILD_DIR)/etudiant.o

.PHONY: all test memcheck memcheck-tests memcheck-run memcheck-scenario clean run

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/main.o: src/main.c include/projet/etudiant.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/etudiant.o: src/etudiant.c include/projet/etudiant.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(PROGRAM): $(OBJS) | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $^ $(LDLIBS) -o $@

run: $(PROGRAM)
	./$(PROGRAM)

test: $(PROGRAM)
	./$(PROGRAM) | grep -q "Ada: 15.50"

memcheck: memcheck-tests

memcheck-tests: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM)

memcheck-run: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(ARGS)

memcheck-scenario: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(SCENARIO_ARGS)

clean:
	rm -rf $(BUILD_DIR)
