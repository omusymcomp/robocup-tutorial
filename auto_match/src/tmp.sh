# 任意のチームだけ試合を実行するスクリプト

#!/bin/bash -eu

# 2team_helios_autogameの引数
#第1引数 試合数
#第2引数 対戦相手(片方はHELIOS固定)

# 開始時刻を記録
start_time=$(date +%s)

# 現状の仕様だとできチームに合わせて-tオプションを変更できないので注意
~/rcss/work/autogame/src/fixed_teams_autogame.sh helios2022 cyrus2022 2000
~/rcss/work/autogame/src/fixed_teams_autogame.sh helios2022 yushan2022 1000

# 終了時刻を記録
end_time=$(date +%s)

# 実行時間を計算（秒単位）
execution_time=$((end_time - start_time))

# 秒数を時間、分、秒に変換
hours=$((execution_time / 3600))
minutes=$(( (execution_time % 3600) / 60 ))
seconds=$((execution_time % 60))

# 実行時間を時間：分：秒の形式で表示
echo "スクリプトの実行時間: ${hours}時間 ${minutes}分 ${seconds}秒"