#!/bin/bash
# This script gets EAGLE to export a parts list
# This process is complicated because EAGLE has a bug that causes
# it to continuously execute the script telling it to export the list.
# Also, if Xvfb is available, this script will run eagle in that so it
# doesn't offend the user.

EAGLE_JOB="%1"
XVFB=0

if ( which Xvfb > /dev/null 2>&1 )
    then
    AUTH=`mktemp`
    echo localhost > $AUTH
    Xvfb -auth $AUTH :1 > /dev/null 2>&1 &
    export DISPLAY=:1
    EAGLE_JOB="%2"
    XVFB=1
fi

if [ -f $2 ]
then
    rm -f $2
fi

scr=`mktemp`
echo "export partlist $2;" > $scr

EAGLE=eagle
if [[ `./eagle_ver $1 | cut -d . -f 1` == "5" ]]
    then
    EAGLE=eagle5
fi

echo Running EAGLE
$EAGLE $1 -S $scr &

while [ ! -f $2 ]
do
    sleep 0.1
done
kill -9 $EAGLE_JOB

rm $scr

# Kill the X server
if [[ "$XVFB" == "1" ]]
    then
    kill -9 %1
fi
