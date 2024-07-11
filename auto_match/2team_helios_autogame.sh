#!/bin/bash

#第1引数 試合数
#第2引数 対戦相手(片方はHELIOS固定)


#日付のファイルを指定場所に作る
DATE=`date +%Y%m%d%0k%M`
LOGDIR="${HOME}/rcss/log_analysis/log/${DATE}"
mkdir -p ${LOGDIR}

#Git管理している方のHELIOSのパス
Team_L="'${HOME}/rcss/HELIOS/helios/src/start-ocl.sh -t HELIOS2023'"
# 実行スクリプト名が「start.shである前提」
#Team_R="${HOME}/rcss/teams/$2/start.sh"
Team_R="${HOME}/rcss/teams/$2/src/start.sh"

# 相対パスで書かれているバイナリがあるのでcdで移動する
cd "${HOME}/rcss/teams/$2/"
echo $1
count=1
# 各試合回数はこのスクリプト実行時の1つ目の引数で指定
while [[ $count -le $1 ]] ; do	#-leは<=の意味
	echo "--------------------"
	echo " ${Team_L} vs ${Team_R}"
	echo " Game ${count}"
	echo "--------------------"

	DATE=`date +%Y%m%d%0k%M`
	mode=true
	# 2022より前のバイナリ実行時はmin_dash_powerを-100にすること
	# 前半だけで実行したい時はgame_loggingを1にする
	$HOME/rcss/tools/bin/rcssserver server::auto_mode = 1 \
				server::synch_mode = ${mode} \
				server::team_l_start = ${Team_L} server::team_r_start = ${Team_R} \
				server::kick_off_wait = 50 \
				server::half_time = 300 \
				server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 \
				server::penalty_shoot_outs = 0 \
				server::game_logging = 1 server::text_logging = 1 \
				server::game_log_dir = "${LOGDIR}" server::text_log_dir = "${LOGDIR}" \
				server::min_dash_power = -100 \
				2>&1 | tee ${LOGDIR}/${DATE}_match${count}.log
	
	count=$(($count+1))
	sleep 0.1
done

