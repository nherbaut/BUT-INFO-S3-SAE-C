EXERCISES := \
	exercices/seance-01/moyenne \
	exercices/seance-01/max3 \
	exercices/seance-02/compilation-separee \
	exercices/seance-03/swap \
	exercices/seance-04/tableau-dynamique \
	exercices/seance-05/etudiants

PROJECT := projet/starter
COURSES := $(wildcard cours/*.md)
BUILD_DIR := build/supports

.PHONY: all run test memcheck clean supports check-runtime $(EXERCISES) $(PROJECT)

all: $(EXERCISES) $(PROJECT)

$(EXERCISES):
	$(MAKE) -C $@

$(PROJECT):
	$(MAKE) -C $@

run:
	for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir run; done

test:
	for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir test; done

memcheck:
	for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir memcheck; done

supports: $(COURSES)
	python3 tools/build_supports.py

check-runtime:
	python3 tools/check_runtime.py

clean:
	for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir clean; done
	rm -rf build
