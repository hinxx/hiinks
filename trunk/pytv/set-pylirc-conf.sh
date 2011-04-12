#!/bin/sh
#
# Hinko Kocevar, 12 Apr 2010
#
# Look into config folder and set pylirc.conf accordingly.
#
# Version 1

if [ $# -lt 1 ]
then
	echo "Usage: $0 <remote>"
	echo
	echo "<remote>:"
	for r in $(cd config && ls -1)
	do
		r=$(echo $r | cut -f3 -d'.')
		echo " $r"
	done
	exit 1
fi

remote="$1"
echo "Trying to set remote $remote .."

if [ -f src/pylirc.conf ]
then
	echo "pylirc.conf exists."
	exit 0
fi

if [ -f config/pylirc.conf.$remote ]
then
	cp config/pylirc.conf.$remote src/pylirc.conf
else
	echo "pylirc.conf.$remote does not exist."
	exit 1
fi

echo "Success!"
exit 0

