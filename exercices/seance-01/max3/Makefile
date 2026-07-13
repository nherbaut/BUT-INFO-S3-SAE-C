include ../../common.mk

TARGET := max3

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) $< -o $@

run: $(TARGET)
	printf "3 9\n" | ./$(TARGET)

test: $(TARGET)
	printf "3 9\n" | ./$(TARGET) | grep -q "max = 9"

memcheck: $(TARGET)
	printf "3 9\n" | $(VALGRIND) $(VALGRIND_FLAGS) ./$(TARGET)

clean:
	rm -f $(TARGET)
