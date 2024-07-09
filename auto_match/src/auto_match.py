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



if __name__ == "__main__":
    main()