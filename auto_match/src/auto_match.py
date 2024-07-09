import subprocess
import argparse
import sys
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="$HOME/rcss", help="環境構築されているベースディレクトリを指定")
    parser.add_argument("-l", "--left_team_name", dest="left_team_name", default="cyrus2022", help="左側のチーム名を指定")
    parser.add_argument("-r", "--right_team_name", dest="right_team_name", default="yushan2022", help="右側のチーム名を指定")
    args = parser.parse_args()
    setup_tools = AutoMatch(args)



class AutoMatch:
    def __init__(self, args):
        now = datetime.now()
        formatted_date_time = now.strftime("%Y_%m%d_%H%M_%S")
        self.log_dir = args.base_dir + "/log_analysis/log/" + formatted_date_time
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

    def execute_matches():
        pass


if __name__ == "__main__":
    main()