CC=g++
CFLAGS=-I. -Ofast -std=c++11

DEPS = kbd.hpp
OBJ = knight_charm.o  

all: knight_charm

kbd.hpp: knights_charm.py
	python knights_charm.py generate kbd.hpp

%.o: %.cpp $(DEPS)
		$(CC) $(CFLAGS) -c -o $@ $< 

knight_charm: $(OBJ)
		g++ $(CFLAGS) -o $@ $^ 

clean:
	rm knight_charm $(OBJ)
