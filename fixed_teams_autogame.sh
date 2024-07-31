#!/bin/bash

#第1引数 左側のチーム
#第2引数 右側のチーム
#第3引数 試合数

cd `dirname $0`

TEAM_PATH_FILE="team_paths.conf"

BASEDIR="${HOME}/rcss/teams"

# 設定ファイルの読み込み
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Error: Configuration file $CONFIG_FILE does not exist."
  exit 1
fi

#日付のファイルを指定場所に作る
DATE=`date +%Y%m%d%0k%M`
LOGDIR="${HOME}/rcss/log_analysis/log/${DATE}"
mkdir -p ${LOGDIR}

# すべてのチームバイナリが「start.sh」で動くことが前提
Team_L=$1
Team_R=$2
count=1


# チームのスクリプトパスを取得する関数
get_team_script_path() {
  local team=$1
  local path=$(grep "^${team}=" "$CONFIG_FILE" | cut -d'=' -f2)
  echo "$path"
}

# 左チームのスクリプトパスを取得
LEFT_SCRIPT=$(get_team_script_path "$Team_L")
if [ -z "$LEFT_SCRIPT" ]; then
  echo "Error: No script path found for team $Team_L."
  exit 1
fi

# 右チームのスクリプトパスを取得
RIGHT_SCRIPT=$(get_team_script_path "$Team_R")
if [ -z "$RIGHT_SCRIPT" ]; then
  echo "Error: No script path found for team $Team_R."
  exit 1
fi

# 左チームのスクリプトの存在確認
if [ ! -f "$LEFT_SCRIPT" ]; then
  echo "Error: Script $LEFT_SCRIPT does not exist for team $Team_L."
  exit 1
fi

# 右チームのスクリプトの存在確認
if [ ! -f "$RIGHT_SCRIPT" ]; then
  echo "Error: Script $RIGHT_SCRIPT does not exist for team $Team_R."
  exit 1
fi

# 各試合回数はこのスクリプト実行時の3つ目の引数で指定
while [ $count -le $0 ] ; do	#-leは<=の意味
	echo "--------------------"
	echo " ${Team_L} vs ${Team_R}"
	echo " Game ${count}"
	echo "--------------------"
	count=$(($count+1))
	DATE=`date +%Y%m%d%0k%M`
	mode=true
	#  シンクモードをtrueにするかどうか
	synch=true
	#　ログを圧縮するかどうか 0 -> 圧縮, 1 -> 圧縮しない
	COMPRESS=0

	# 試合を実行するチームがすべてsynch_modeに対応していることが前提
	rcssserver server::auto_mode = ${mode} \
				server::synch_mode = ${synch} \
				server::team_l_start = ${LEFT_SCRIPT} server::team_r_start = ${RIGHT_SCRIPT} \
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
