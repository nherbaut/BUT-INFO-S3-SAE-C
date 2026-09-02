CC ?= cc
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic -g
VALGRIND ?= valgrind
VALGRIND_FLAGS ?= \
	--leak-check=full \
	--show-leak-kinds=all \
	--track-origins=yes \
	--error-exitcode=1

BUILD_DIR := build
PROGRAM := $(BUILD_DIR)/diagnostiquer-valgrind
SCENARIO ?= fuite
SCENARIOS := fuite pointeur-perdu double-free apres-free

.PHONY: all run test memcheck clean $(addprefix memcheck-,$(SCENARIOS))

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(PROGRAM): src/main.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

run: $(PROGRAM)
	./$(PROGRAM) $(SCENARIO)

test: $(PROGRAM)
	./$(PROGRAM) aide

memcheck: $(PROGRAM)
	@status=0; for scenario in $(SCENARIOS); do \
		$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $$scenario || status=1; \
	done; exit $$status

memcheck-%: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $*

clean:
	rm -rf $(BUILD_DIR)
