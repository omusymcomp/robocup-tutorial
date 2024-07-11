#!/bin/bash

#第1引数 試合数

#チームをリストで渡す
Team="${HOME}/rcss/teams/*"	#*を付けると中にあるファイル全部持ってきてくれる

#日付のファイルを指定場所に作る
DATE=`date +%Y%m%d%0k%M`
LOGDIR="${HOME}/rcss/log_analysis/log/${DATE}"
mkdir -p ${LOGDIR}

#スペースで分割してTeam_Listに入れる
Team_List=(${Team/ /})

# synch modeで実行できないチーム
not_synch_mode=("Gliders2016" "fra-united2022" "oxsy2022")
# 実行せずに飛ばすチーム
skip_teams_array=("not_use" "base_team" "helios2022" "helios2017" "namira2018" "namira2018")

# game loop
for ((i=0; i<(${#Team_List[@]}); i++)) do
	# すべてのチームバイナリが「start.sh」で動くことが前提
	Team_L="'${HOME}/rcss/HELIOS/helios/src/start-ocl.sh'"
	Team_R="${Team_List[${i}]}/start.sh"
	cd ${Team_List[${i}]}
	count=1
	skip=false
	mode=true

	# IFSを一時的に変更して文字列を分割
	IFS="/" read -ra elements <<< "${Team_List[${i}]}"
	Team_Name=${elements[-1]}

	# 試合を行わないチームの検出
	for skip_team in "${skip_teams_array[@]}"
	do
	if [ "$skip_team" = "$Team_Name" ]; then
		skip=0
		skip=true
		break
	fi
	done

	if "${skip}"; then
		continue
	fi

	# sych_modeで起動できないチームの検出
	for not_synch_team in "${not_synch_mode[@]}"
	do
	if [ "$not_synch_team" = "$Team_Name" ]; then
		mode=false
		break
	fi
	done

	# 各試合回数はこのスクリプト実行時の1つ目の引数で指定
	while [ $count -le $1 ] ; do	#-leは<=の意味
		echo "--------------------"
		echo " ${Team_L} vs ${Team_R}"
		echo " Game ${count}"
		echo "--------------------"
		
		DATE=`date +%Y%m%d%0k%M`
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
					2>&1 | tee ${LOGDIR}/${Team_Name}_match${count}.log
		
		count=$(($count+1))
		sleep 0.1
	done
done