#!/bin/bash -eu

#第1引数 左側のチーム
#第2引数 右側のチーム
#第3引数 試合数

BASEDIR="${HOME}/rcss/teams/"

#日付のファイルを指定場所に作る
DATE=`date +%Y%m%d%0k%M`
LOGDIR="${HOME}/rcss/log_analysis/log/${DATE}"
mkdir -p ${LOGDIR}

# すべてのチームバイナリが「start.sh」で動くことが前提
Team_L="${BASEDIR}/$1/start.sh"
Team_R="${BASEDIR}/$2/start.sh"
count=1

# 相対パスで書かれているバイナリがあるのでcdで移動する
cd "${BASEDIR}/$2/"

# 各試合回数はこのスクリプト実行時の1つ目の引数で指定
while [ $count -le $3 ] ; do	#-leは<=の意味
	echo "--------------------"
	echo " ${Team_L} vs ${Team_R}"
	echo " Game ${count}"
	echo "--------------------"
	
	DATE=`date +%Y%m%d%0k%M`
	mode=true

	# 試合を実行するチームがすべてsynch_modeに対応していることが前提
	$HOME/rcss/tools/bin/rcssserver server::auto_mode = 1 \
				server::synch_mode = ${mode} \
				server::team_l_start = ${Team_L} server::team_r_start = ${Team_R} \
				server::kick_off_wait = 50 \
				server::half_time = 300 \
				server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 \
				server::penalty_shoot_outs = 0 \
				server::game_logging = 1 server::text_logging = 1 \
				server::game_log_dir = "${LOGDIR}" server::text_log_dir = "${LOGDIR}" \
				2>&1 | tee ${LOGDIR}/${DATE}_match${count}.log
	
	count=$(($count+1))
	sleep 0.1
done