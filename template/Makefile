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
PROGRAM := $(BUILD_DIR)/projet-cli
TEST_PROGRAM := $(BUILD_DIR)/test-greet

.PHONY: all test memcheck memcheck-tests memcheck-run memcheck-scenario clean run

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/greet.o: src/greet.c include/projet/greet.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(PROGRAM): src/main.c $(BUILD_DIR)/greet.o | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(TEST_PROGRAM): tests/test_greet.c $(BUILD_DIR)/greet.o | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) $(LDFLAGS) $^ $(LDLIBS) -o $@

test: $(TEST_PROGRAM)
	./$(TEST_PROGRAM)

run:
	$(PROGRAM)

# Convention : "memcheck" valide la mémoire pendant les tests unitaires.
memcheck: memcheck-tests

memcheck-tests: $(TEST_PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TEST_PROGRAM)

# Exécution normale sous Valgrind, avec arguments fournis par l'utilisateur.
# Exemple : make memcheck-run ARGS="arg1 arg2"
memcheck-run: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(ARGS)

# Scénario fixe, reproductible et adapté à l'intégration continue.
memcheck-scenario: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(SCENARIO_ARGS)

clean:
	rm -rf $(BUILD_DIR)
