CC ?= cc
CPPFLAGS ?= -Iinclude -Iprovided/cjson $(shell pkg-config --cflags libcurl)
CFLAGS ?= -std=c11 -Wall -Wextra -Wpedantic
LDFLAGS ?=
LDLIBS ?= -lm $(shell pkg-config --libs libcurl)

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
PROGRAM := $(BUILD_DIR)/capteurs
TEST_STATISTICS := $(BUILD_DIR)/test_statistics
TEST_SERIES := $(BUILD_DIR)/test_series
TEST_SOURCE := $(BUILD_DIR)/test_source
LIB_OBJS := \
	$(BUILD_DIR)/series.o \
	$(BUILD_DIR)/statistics.o \
	$(BUILD_DIR)/sensor_source.o \
	$(BUILD_DIR)/report.o \
	$(BUILD_DIR)/cJSON.o

.PHONY: all run test test-statistics test-series test-source memcheck memcheck-tests memcheck-run memcheck-scenario clean student-tarball

all: $(PROGRAM)

$(BUILD_DIR):
	mkdir -p $@

$(BUILD_DIR)/main.o: src/main.c include/projet/report.h include/projet/sensor_source.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/series.o: src/series.c include/projet/series.h include/projet/measure.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/statistics.o: src/statistics.c include/projet/statistics.h include/projet/series.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/sensor_source.o: provided/sensor_source.c include/projet/sensor_source.h include/projet/series.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/cJSON.o: provided/cjson/cJSON.c provided/cjson/cJSON.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/report.o: src/report.c include/projet/report.h include/projet/statistics.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_statistics.o: tests/test_statistics.c include/projet/statistics.h include/projet/series.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_series.o: tests/test_series.c include/projet/series.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(BUILD_DIR)/test_source.o: tests/test_source.c include/projet/sensor_source.h | $(BUILD_DIR)
	$(CC) $(CPPFLAGS) $(CFLAGS) -c $< -o $@

$(PROGRAM): $(BUILD_DIR)/main.o $(LIB_OBJS)
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(TEST_STATISTICS): $(BUILD_DIR)/test_statistics.o $(BUILD_DIR)/statistics.o
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(TEST_SERIES): $(BUILD_DIR)/test_series.o $(BUILD_DIR)/series.o

	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

$(TEST_SOURCE): $(BUILD_DIR)/test_source.o $(BUILD_DIR)/series.o $(BUILD_DIR)/sensor_source.o $(BUILD_DIR)/cJSON.o
	$(CC) $(LDFLAGS) $^ $(LDLIBS) -o $@

run: $(PROGRAM)
	./$(PROGRAM)

test: test-statistics test-series test-source

test-statistics: $(TEST_STATISTICS)
	./$(TEST_STATISTICS)

test-series: $(TEST_SERIES)
	./$(TEST_SERIES)

test-source: $(TEST_SOURCE)
	./$(TEST_SOURCE)

memcheck: memcheck-tests

memcheck-tests: $(TEST_STATISTICS) $(TEST_SERIES) $(TEST_SOURCE)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TEST_STATISTICS)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TEST_SERIES)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TEST_SOURCE)

memcheck-run: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(ARGS)

memcheck-scenario: $(PROGRAM)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(PROGRAM) $(SCENARIO_ARGS)

student-tarball:
	python3 ../../tools/export_capteurs_starter.py

clean:
	rm -rf $(BUILD_DIR)
