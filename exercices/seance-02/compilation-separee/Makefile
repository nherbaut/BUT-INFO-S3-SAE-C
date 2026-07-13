include ../../common.mk

TARGET := stats
OBJS := main.o stats.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

main.o: main.c stats.h
	$(CC) $(CFLAGS) -c main.c

stats.o: stats.c stats.h
	$(CC) $(CFLAGS) -c stats.c

run: $(TARGET)
	./$(TARGET)

test: $(TARGET)
	./$(TARGET) | grep -q "moyenne = 12.00"

memcheck: $(TARGET)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TARGET)

clean:
	rm -f $(TARGET) $(OBJS)

