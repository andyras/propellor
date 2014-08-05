### This line should be just about all you have to change ######################
# name of main executable
BIN = propellor
################################################################################

#DEBUG_MAKE = "foo"

# directories for headers, objects and source files
INCDIR = ./include
OBJDIR = ./obj
SRCDIR = ./src
LIBDIR = ./lib
BINDIR = ./bin

# compiler and archiver
CPP = g++-4.9
AR = ar

CPPFLAGS = -O3 -Wall -std=c++11 -fopenmp
INCLUDES = -I$(INCDIR) -I/usr/local/Cellar/eigen/3.2.1/include/eigen3/

ifdef DEBUG_MAKE
  CPPFLAGS += -pg -g -debug
  LDFLAGS += -pg -g -debug
endif

# make will look for .cpp files in $(SRCDIR)
vpath %.cpp $(SRCDIR)

# list of source files
SOURCES = $(wildcard $(SRCDIR)/*.cpp)

# object files have same name as .cpp files, but with .o extension
OBJECTS = $(patsubst $(SRCDIR)/%.cpp,obj/%.o,$(SOURCES))

# build the main executable; this should be listed first
$(BINDIR)/$(BIN): $(OBJECTS) $(BINDIR)
	$(CPP) -o $@ $(OBJECTS) $(LDFLAGS) -fopenmp

# automatic rule for building objects
$(OBJDIR)/%.o: %.cpp
	$(CPP) $(CPPFLAGS) $(INCLUDES) -c $< -o $@

# all objects depend on object directory
$(OBJECTS): | $(OBJDIR)

# add all obj files except main to library
library: $(OBJECTS) $(LIBDIR)
	find $(OBJDIR) -name *.o ! -name main.o | xargs $(AR) vrs $(LIBDIR)/lib$(BIN).a

.PHONY: clean install uninstall $(BINDIR) $(OBJDIR) $(LIBDIR)

clean:
	rm -rf $(BINDIR)
	rm -rf $(OBJDIR)
	rm -rf $(LIBDIR)

install: $(BIN) | $(BINDIR)
	cp dynamix $(BINDIR)

uninstall:
	rm -rf $(BINDIR)/$(BIN)

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(BINDIR):
	mkdir -p $(BINDIR)

$(LIBDIR):
	mkdir -p $(LIBDIR)
