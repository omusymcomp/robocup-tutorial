#!/bin/bash

#第1引数 左側のチーム
#第2引数 右側のチーム
#第3引数 試合数

BASEDIR=${HOME}/rcss/teams/robocup2024

#日付のファイルを指定場所に作る
DATE=`date +%Y%m%d%0k%M`
LOGDIR="${HOME}/rcss/log_analysis/log/${DATE}"
mkdir -p ${LOGDIR}

# すべてのチームバイナリが「start.sh」で動くことが前提
Team_L="${BASEDIR}/$1/bin/start.sh"
Team_R="${BASEDIR}/$2/bin/start.sh"
count=1

# 各試合回数はこのスクリプト実行時の1つ目の引数で指定
while [ $count -le $3 ] ; do	#-leは<=の意味
	echo "--------------------"
	echo " ${Team_L} vs ${Team_R}"
	echo " Game ${count}"
	echo "--------------------"
	count=$(($count+1))
	DATE=`date +%Y%m%d%0k%M`
	mode=true
	#　ログを圧縮するかどうか 0 -> 圧縮, 1 -> 圧縮しない
	COMPRESS=0

	# 試合を実行するチームがすべてsynch_modeに対応していることが前提
	rcssserver server::auto_mode = ${mode} \
				server::synch_mode = ${mode} \
				server::team_l_start = ${Team_L} server::team_r_start = ${Team_R} \
				server::kick_off_wait = 50 \
				server::half_time = 300 \
				server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 \
				server::penalty_shoot_outs = 0 \
				server::game_logging = ${mode} server::text_logging = ${mode} \
				server::game_log_dir = "${LOGDIR}" server::text_log_dir = "${LOGDIR}" \
				server::game_log_compression=${COMPRESS} \
	        	server::text_log_compression=${COMPRESS} &
				2>&1 | tee ${LOGDIR}/${DATE}.log
	sleep 0.1
done
