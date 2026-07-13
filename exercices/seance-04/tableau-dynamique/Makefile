include ../../common.mk

TARGET := tableau

all: $(TARGET)

$(TARGET): main.c
	$(CC) $(CFLAGS) $< -o $@

run: $(TARGET)
	./$(TARGET)

test: $(TARGET)
	./$(TARGET) | grep -q "taille=5 somme=15"

memcheck: $(TARGET)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TARGET)

clean:
	rm -f $(TARGET)

