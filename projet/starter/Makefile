CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -pedantic -g
VALGRIND ?= valgrind
VALGRIND_FLAGS ?= --leak-check=full --error-exitcode=1

APP := carnet
TEST_APP := test_carnet
OBJS := src/carnet.o

.PHONY: all run test memcheck clean

all: $(APP) $(TEST_APP)

$(APP): src/main.o $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

$(TEST_APP): tests/test_carnet.o $(OBJS)
	$(CC) $(CFLAGS) $^ -o $@

src/main.o: src/main.c src/carnet.h
	$(CC) $(CFLAGS) -c $< -o $@

src/carnet.o: src/carnet.c src/carnet.h
	$(CC) $(CFLAGS) -c $< -o $@

tests/test_carnet.o: tests/test_carnet.c src/carnet.h
	$(CC) $(CFLAGS) -Isrc -c $< -o $@

run: $(APP)
	./$(APP)

test: $(TEST_APP)
	./$(TEST_APP)

memcheck: $(APP) $(TEST_APP)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(APP)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TEST_APP)

clean:
	rm -f $(APP) $(TEST_APP) src/*.o tests/*.o

