CC ?= gcc
CFLAGS ?= -std=c11 -Wall -Wextra -pedantic -g
VALGRIND ?= valgrind
VALGRIND_FLAGS ?= --leak-check=full --error-exitcode=1

.PHONY: all run test memcheck clean

