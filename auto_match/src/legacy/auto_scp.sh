#!/bin/sh

PW="9GSymComp"
USER_NAME="hatakeyama"
ADDRESS="192.168.2.40"
LOGDIR="~/rcss/autogame/slackserver/log/RoboCup2022"
Folder_Name=$1
#計算機側で下記の代入ができれば自動的に最新ファイルを取ってこれる
#File_Path = ls -rt | tail -n -1


expect -c "
set timeout 5
spawn scp -r ${USER_NAME}@${ADDRESS}:${LOGDIR}/${Folder_Name}/ $HOME/rcss/log_analysis/log
expect \"password:\"
send \"${PW}\n\"
interact"

