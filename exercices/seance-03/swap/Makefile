include ../../common.mk

TARGET := swap

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

test: $(TARGET)
	./$(TARGET) | grep -q "apres swap_ptr: a=2 b=1"

memcheck: $(TARGET)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TARGET)

clean:
	rm -f $(TARGET)

