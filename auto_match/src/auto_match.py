import subprocess
import argparse
import sys
import os
from datetime import datetime
import getpass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="$HOME/rcss", 
                        help="環境構築されているベースディレクトリを指定")
    parser.add_argument("-l", "--left_team_name", dest="left_team_name", default="helios2022", 
                        choices=["HELIOS", "HELIOS-Base", "yushan2022", "cyrus2022", 
                                 "helios2022", "fra-united2022", "alice2022"], help="左側のチーム名を指定")
    parser.add_argument("-r", "--right_team_name", dest="right_team_name", default="cyrus2022", 
                        choices=["HELIOS", "HELIOS-Base", "yushan2022", "cyrus2022", 
                                 "helios2022", "fra-united2022", "alice2022"], help="右側のチーム名を指定")
    parser.add_argument("-n", "--match_number", dest="match_number", default=3, type=int, 
                        help="試合を行う回数を指定する")
    
    args = parser.parse_args()
    auto_match = AutoMatch(args)
    auto_match.execute_matches(args)



class AutoMatch:
    def __init__(self, args):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y_%m%d_%H%M_%S")
        self.log_dir = args.base_dir + "/log_analysis/log/" + self.formatted_date_time
        self.team_binary_dir = args.base_dir + "/teams"
        self.left_team_dir = f"{self.team_binary_dir}/{args.left_team_name}/start.sh" if self.is_binary_team(args.left_team_name) \
                                                                                      else f"{args.base_dir}/{args.left_team_name}/{args.left_team_name.lower()}/src/start.sh" 
        self.right_team_dir = f"{self.team_binary_dir}/{args.right_team_name}/start.sh" if self.is_binary_team(args.right_team_name) \
                                                                                      else f"{args.base_dir}/{args.right_team_name}/{args.right_team_name.lower()}/src/start.sh"
        self.output_text = None

    def is_binary_team(self, team_name):
        # バイナリだけのチームなのか、ソースコードもあるチームなのかを判定する
        # TODO：HAMも実装するなら条件文に追加する
        if team_name == "HELIOS" or team_name == "HELIOS-Base":
            return False
        else:
            return True

    def run_command(self, command):
        try:
            # shell=TrueはOSコマンドインジェクションの恐れがあるので要注意
            # 現状は各個人で使うので問題ないはず
            self.output_text = subprocess.run(command, check=True, text=True, shell=True, stdout=subprocess.PIPE).stdout
            print(self.output_text)
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
                                                                   f"server::game_log_dir = {self.log_dir} server::text_log_dir = {self.log_dir} "

            self.run_command(f"{execute_command}")
            self.output_log(counter)

    def output_log(self, counter):
        # ファイル端末出力の内容を書き込む
        with open(f"/home/{getpass.getuser()}/rcss/log_analysis/log/{self.formatted_date_time}/{self.formatted_date_time}_match{counter}.log", "w") as log_file:
            log_file.write(self.output_text)


if __name__ == "__main__":
    main()