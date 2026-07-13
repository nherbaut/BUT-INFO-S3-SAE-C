include ../../common.mk

TARGET := moyenne

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) $< -o $@

run: $(TARGET)
	printf "12 14\n" | ./$(TARGET)

test: $(TARGET)
	printf "12 14\n" | ./$(TARGET) | grep -q "moyenne = 13"

memcheck: $(TARGET)
	printf "12 14\n" | $(VALGRIND) $(VALGRIND_FLAGS) ./$(TARGET)

clean:
	rm -f $(TARGET)
