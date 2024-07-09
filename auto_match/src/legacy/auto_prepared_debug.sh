#!/bin/sh

# ./auto_prepared_debug.sh オフラインデバッグモードの実行回数

DATE=`date +%Y%m%d%0k%M`
File_Name="output_offlinelog_${DATE}"
Save_Dir="${HOME}/rcss/autogame/data/"

cd $HOME/rcss/HELIOS/helios
./configure --with-librcsc=$HOME/local
make
for i in `seq $1`
do
    cd $HOME/rcss/autogame/src
    ./2team_helios_autogame.sh 1
    cd $HOME/rcss/HELIOS/helios/src
    ./start-offline.sh >> "${Save_Dir}${File_Name}.txt"
    echo " " >> "${Save_Dir}${File_Name}.txt"
done
echo "process finished!"
#soccerwindow2
