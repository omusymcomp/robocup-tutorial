#!/bin/bash
time_start=`date +%s`

#!/bin/bash

#第1引数 左側のチーム
#第2引数 試合数

BASEDIR=${HOME}/rcss/

#日付のファイルを指定場所に作る
DATE=`date +%Y%m%d%0k%M`
LOGDIR="${BASEDIR}/log_data/${DATE}"
mkdir -p ${LOGDIR}

# すべてのチームバイナリが「start.sh」で動くことが前提
Team_L="${BASEDIR}/teams/robocup2022/$1/bin/start.sh"
Team_R="${BASEDIR}/teams/base_team/helios-base/src/start.sh"
count=1

# 各試合回数はこのスクリプト実行時の1つ目の引数で指定
while [ $count -le $2 ] ; do	#-leは<=の意味
	echo "--------------------"
	echo " ${Team_L} vs ${Team_R}"
	echo " Game ${count}"
	echo "--------------------"
	count=$(($count+1))
	DATE=`date +%Y%m%d%0k%M`
	mode=true

	# 試合を実行するチームがすべてsynch_modeに対応していることが前提
	rcssserver server::auto_mode = 1 \
				server::synch_mode = ${mode} \
				server::team_l_start = ${Team_L} server::team_r_start = ${Team_R} \
				server::kick_off_wait = 50 \
				server::half_time = 300 \
				server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 \
				server::penalty_shoot_outs = 0 \
				server::game_logging = 1 server::text_logging = 1 \
				server::game_log_dir = "${LOGDIR}" server::text_log_dir = "${LOGDIR}" \
				2>&1 | tee ${LOGDIR}/${DATE}.log
	sleep 0.1
done

time_end=`date +%s`
PT=`expr ${time_end} - ${time_start}`
H=`expr ${PT} / 3600`
PT=`expr ${PT} % 3600`
M=`expr ${PT} / 60`
S=`expr ${PT} % 60`
echo "${H}時間${M}分${S}秒"