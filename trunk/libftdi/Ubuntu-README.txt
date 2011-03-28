	libftdi (from http://www.intra2net.com/en/developer/libftdi/)

Date: 28 Mar 2011


Under Ubuntu 10.10 current version of libftdi is 0.18. It provides following DEBs:

libftdi1_0.18-1
libftdi-dev_0.18-1
libftdipp1_0.18-1
libftdipp-dev_0.18-1
python-ftdi_0.18-1

At least a change to Python bindings is required to make Python libftdi usable.

The libftdi sources found here were taken from:
 - Ubuntu 10.10 libftdi-0.18-1 source
 - upstream libftdi GIT tree (on 28 Mar 2011)

Version was bumped to 0.18-2.

Building DEB from source:

$ cd libftdi-0.18
$ dpkg-buildpackage -rfakeroot -uc -b

Produces:
$ ls -1 ../*.deb
../libftdi1_0.18-2_i386.deb
../libftdi-dev_0.18-2_i386.deb
../libftdipp1_0.18-2_i386.deb
../libftdipp-dev_0.18-2_i386.deb
../python-ftdi_0.18-2_i386.deb

