CC := g++

OBJS := main.o

app.exe : $(OBJS)
	$(CC) $^ -o $@ -pthread

%.o : %.c
	$(CC) -c -O1 $<

.PHONY : clean

clean :
	rm *.o *.exe
