include ../../common.mk

TARGET := etudiants
OBJS := main.o etudiant.o

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $@

main.o: main.c etudiant.h
	$(CC) $(CFLAGS) -c main.c

etudiant.o: etudiant.c etudiant.h
	$(CC) $(CFLAGS) -c etudiant.c

run: $(TARGET)
	./$(TARGET)

test: $(TARGET)
	./$(TARGET) | grep -q "Ada: 15.50"

memcheck: $(TARGET)
	$(VALGRIND) $(VALGRIND_FLAGS) ./$(TARGET)

clean:
	rm -f $(TARGET) $(OBJS)

