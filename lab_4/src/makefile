CC := g++

OBJS := main.o

app.exe : $(OBJS)
	$(CC) $^ -o $@ -pthread

%.o : %.c
	$(CC) -c $<

.PHONY : clean

clean :
	rm *.o *.exe
