
CC = gcc
CFLAGS = -g -Wall

# Linking options:
LDFLAGS =

# List the libraries you need to link with in LDLIBS.
# For example, use -lm for the math library.
LDLIBS =

# The first target gets built when you run make.
# It's usually your executable (myprogram in this case).
#
# Note that we did not specify the linking recipe.
# Instead, we rely on one of Make's implicit rules:
#
#     $(CC) $(LDFLAGS) <dependent-.o-files> $(LDLIBS) -o <executable-name>
#
myprogram: myprogram.o process.o

# myprogram.o depends not only on myprogram.c, but also on myadd.h, which it
# includes.  myprogram.o will be recompiled if it has an earlier timestamp than
# any of its dependencies.
#
# Make uses the following implicit rule to compile a .c file into a .o file:
#
#     $(CC) -c $(CFLAGS) -o <target-.o-file> <the-.c-file>
#
# Make's implicit rule assumes myprogram.o depends on myprogram.c, so we can
# omit myprogram.c in the dependency list if we want to.
myprogram.o: myprogram.c process.h

# myadd.o depends on myadd.c and myadd.h.
process.o: process.c process.h


# Always provide the "clean" target that removes build artifacts (e.g., the
# target executable and .o files) and other garbage that may be created during
# the development process.
#
# The "clean" target does not correspond to a filename, so we tell Make that
# it's a "phony" target, meaning it does not need to check the timestamp of
# a file called "clean".
.PHONY: clean
clean:
	rm -f *.o a.out core myprogram

# The "all" target can be useful if your Makefile builds multiple programs.
# Here we'll have it first do "clean", and rebuild the myprogram target.
#
# Like "clean", we declare it as a phony target because it doesn't actually
# build a file named "all".
#
# Dependencies are built in the order they are declared, left to right.
.PHONY: all
all: clean myprogram