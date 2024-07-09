import subprocess
import argparse
import sys
import os
from datetime import datetime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="$HOME/rcss", help="環境構築をするベースディレクトリを指定")
    args = parser.parse_args()
    setup_tools = AutoMatch(args)



class AutoMatch:
    def __init__(self, args):
        now = datetime.now()
        formatted_date_time = now.strftime("%Y_%m%d_%H%M_%S")
        self.log_dir = args.base_dir + "/log_analysis/log/" + formatted_date_time




if __name__ == "__main__":
    main()