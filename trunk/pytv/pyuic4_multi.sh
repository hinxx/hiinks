#!/bin/sh
#
# Hinko Kocevar, 2 Nov 2010
#
# This script will create py file from ui file, and
# fix a bug for importing Qwt5 class.
# Line 'from qwt_plot import QwtPlot' is changed to
# 'from PyQt4.Qwt5 import QwtPlot'.
#
# See http://www.riverbankcomputing.com/pipermail/pyqt/2006-August/013960.html
#

handle () {
	for f in *.ui
	do
		[ ! -f "$f" ] && continue

		o=$(basename "$f" .ui)
		echo "Converting $f --> $o.py"
		pyuic4 "$f" | sed -e 's/qwt_plot/PyQt4.Qwt5/' > $o.py
		ret=$?
		if [ $ret -ne 0 ]
		then
			echo "pyuic4 error $ret"
		 	return $ret
		fi
	done
	
	return 0
}

cwd=$(pwd)
folders="$(find . -type d | grep -v svn)"
for folder in $folders
do
	echo "In folder $folder"
	cd "$folder" || exit $?
	handle || exit $?
	cd "$cwd" || exit $?
done

exit 0

