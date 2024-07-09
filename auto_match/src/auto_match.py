import subprocess
import argparse
import sys
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="$HOME/rcss", help="環境構築されているベースディレクトリを指定")
    parser.add_argument("-l", "--left_team_name", dest="left_team_name", default="helios2022", help="左側のチーム名を指定")
    parser.add_argument("-r", "--right_team_name", dest="right_team_name", default="cyrus2022", help="右側のチーム名を指定")
    parser.add_argument("-n", "--match_number", dest="match_number", default=3, type=int, help="試合を行う回数を指定する")
    args = parser.parse_args()
    setup_tools = AutoMatch(args)
    setup_tools.execute_matches(args)



class AutoMatch:
    def __init__(self, args):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y_%m%d_%H%M_%S")
        self.log_dir = args.base_dir + "/log_analysis/log/" + self.formatted_date_time
        self.team_binary_dir = args.base_dir + "/teams"
        self.left_team_dir = args.base_dir + "/" + args.left_team_name + "/start.sh"
        self.right_team_dir = args.base_dir + "/" + args.right_team_name + "/start.sh"

    def run_command(self, command):
        try:
            # shell=TrueはOSコマンドインジェクションの恐れがあるので要注意
            # 現状は各個人で使うので問題ないはず
            result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
            print(result.stdout)
            print(f"実行が正常に終了しました: {command}\n\n")
        except subprocess.CalledProcessError as e:
            # コマンドがエラーを返した場合
            print(e.stderr)
            print(f"コマンドにエラーが発生しました: {command}\n\n")
        except Exception as e:
            # その他の例外
            print(e.stderr)
            print(f"想定していないエラーが発生しました: {command}\n\n")

    def execute_matches(self, args):
        #os.chdir(f"./librcsc")
        mode = "true"
        for counter in range(args.match_number):
            execute_command = f"{args.base_dir}/tools/bin/rcssserver server::auto_mode = 1 " \
                                                                   f"server::synch_mode = {mode} " \
                                                                   f"server::team_l_start = {self.left_team_dir} server::team_r_start = {self.right_team_dir} " \
                                                                   f"server::kick_off_wait = 50 " \
				                                                   f"server::half_time = 300 " \
				                                                   f"server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 " \
                                                                   f"server::penalty_shoot_outs = 0 " \
                                                                   f"server::game_logging = 1 server::text_logging = 1 " \
                                                                   f"server::game_log_dir = {self.log_dir} server::text_log_dir = {self.log_dir} " \
                                                                   f"2>&1 | tee {self.log_dir}/{self.formatted_date_time}_match{counter}.log"

            self.run_command(f"{execute_command}")


if __name__ == "__main__":
    main()