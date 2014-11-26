#!/bin/bash
# shipit.sh: Grab all the gerbers from the various boards and package
# them up into a zip for shipping.
tdir=`mktemp -d`

for x in power motor pwm jointio
do
    mkdir -p ${tdir}/ship/${x}
    cp ../${x}/pcb/trunk/gerbers/${x}-*.{gbr,drd} ${tdir}/ship/${x}/
done

pushd $tdir
zip -r ship ship
popd

mv ${tdir}/ship.zip ./
rm -rf $tdir
