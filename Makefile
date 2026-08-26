EXERCISES := \
	exercices/seance-01/bonjour \
	exercices/seance-01/moyenne \
	exercices/seance-01/max3 \
	exercices/seance-02/compilation-separee \
	exercices/seance-03/swap \
	exercices/seance-04/tableau-dynamique \
	exercices/seance-05/etudiants

PROJECT := projet/starter
COURSES := $(wildcard cours/*.md)
BUILD_DIR := build/supports
PORT ?= 8000
C_REPL_IMAGE ?= c-repl

.PHONY: all run test memcheck clean supports serve c check-runtime $(EXERCISES) $(PROJECT)

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

serve: supports
	@printf "Site local: http://localhost:%s/\n" "$(PORT)"
	python3 -m http.server $(PORT) --directory $(BUILD_DIR)

c:
	docker run --rm -it $(C_REPL_IMAGE)

check-runtime:
	python3 tools/check_runtime.py

clean:
	for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir clean; done
	rm -rf build
