EXERCISES := \
	exercices/seance-01/bonjour \
	exercices/seance-01/moyenne \
	exercices/seance-01/max3 \
	exercices/seance-02/compilation-separee \
	exercices/seance-03/swap \
	exercices/seance-03/etudiants \
	exercices/seance-04/tableau-dynamique

# Certains starters sont volontairement incomplets et sont validés par les
# étudiants pendant le cours ; ils ne font pas partie de la CI du dépôt.
TEST_EXERCISES := $(filter-out \
	exercices/seance-01/max3 \
	exercices/seance-04/tableau-dynamique, \
	$(EXERCISES))

PROJECT := projet/starter
SENSORS_PROJECT := projet/capteurs-starter
COURSES := $(wildcard cours/*.md)
BUILD_DIR := build/supports
PORT ?= 8000
C_REPL_IMAGE ?= c-repl

.PHONY: all run test memcheck clean supports serve serve-static c check-runtime capteurs capteurs-student-tarball check-tools cppcheck $(EXERCISES) $(PROJECT)

all: $(EXERCISES) $(PROJECT)

$(EXERCISES):
	$(MAKE) -C $@

$(PROJECT):
	$(MAKE) -C $@

run:
	set -e; for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir run; done

test:
	set -e; for dir in $(TEST_EXERCISES) $(PROJECT); do $(MAKE) -C $$dir test; done

memcheck:
	set -e; for dir in $(TEST_EXERCISES) $(PROJECT); do $(MAKE) -C $$dir memcheck; done

supports: $(COURSES)
	python3 tools/build_supports.py

serve:
	python3 tools/serve_live.py --port $(PORT)

serve-static: supports
	@printf "Site local: http://localhost:%s/\n" "$(PORT)"
	python3 -m http.server $(PORT) --directory $(BUILD_DIR)

c:
	docker run --rm -it $(C_REPL_IMAGE)

check-runtime:
	python3 tools/check_runtime.py

capteurs:
	$(MAKE) -C $(SENSORS_PROJECT)

capteurs-student-tarball:
	python3 tools/export_capteurs_starter.py

check-tools:
	$(MAKE) -C $(SENSORS_PROJECT) check-tools

cppcheck:
	$(MAKE) -C $(SENSORS_PROJECT) cppcheck

clean:
	set -e; for dir in $(EXERCISES) $(PROJECT); do $(MAKE) -C $$dir clean; done
	rm -rf build
