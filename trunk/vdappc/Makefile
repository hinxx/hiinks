CC	= gcc
COPTS	= -DBIGENDIAN -O0 -ggdb3
CLIBS	=

all: vdappc.c ppc_disasm.c ppc_disasm.h
	mkdir -p bin
	$(CC) $(COPTS) -o bin/vdappc vdappc.c ppc_disasm.c $(CLIBS)