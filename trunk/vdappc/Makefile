CC	= gcc
COPTS	= -DBIGENDIAN -O2
CLIBS	=

all: vdappc.c ppc_disasm.c ppc_disasm.h
	$(CC) $(COPTS) -o bin/vdappc vdappc.c ppc_disasm.c $(CLIBS)