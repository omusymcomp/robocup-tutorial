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
                        choices=["custom", "HELIOS", "HELIOS-Base", "yushan2022", "cyrus2022", 
                                 "helios2022", "fra-united2022", "alice2022"], help="左側のチーム名を指定")
    parser.add_argument("-r", "--right_team_name", dest="right_team_name", default="cyrus2022", 
                        choices=["custom", "HELIOS", "HELIOS-Base", "yushan2022", "cyrus2022",
                                 "helios2022", "fra-united2022", "alice2022"], help="右側のチーム名を指定")
    #parser.add_argument("-fl", "--fixed_teamname_l", dest="fixed_teamname_l", default="", 
    #                    help="表記上の左側のチームの名前を指定する。デフォルトだと登録されている名前をそのまま利用する")
    #parser.add_argument("-fr", "--fixed_teamname_r", dest="fixed_teamname_r", default="", 
    #                    help="表記上の右側のチームの名前を指定する。デフォルトだと登録されている名前をそのまま利用する")
    parser.add_argument("-n", "--match_number", dest="match_number", default=3, type=int, 
                        help="試合を行う回数を指定する")
    parser.add_argument("--is_synch_mode", action="store_true", dest="is_synch_mode", help="synch_modeで実行する場合に指定する")
    
    args = parser.parse_args()
    auto_match = AutoMatch(args)
    auto_match.execute_matches(args)



class AutoMatch:
    def __init__(self, args):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y_%m%d_%H%M_%S")
        self.log_dir = args.base_dir + "/log_analysis/log/" + self.formatted_date_time
        self.team_binary_dir = args.base_dir + "/teams"
        
        if args.left_team_name == "custom":
            self.left_team_path_list = self.get_custom_team_path_list()
        else:
            self.left_team_path = self.get_team_path(args.base_dir, args.left_team_name)

        self.right_team_path = self.get_team_path(args.base_dir, args.right_team_name)

        self.output_text = None

    def get_custom_team_path_list(self):
        custom_dir = self.change_home_path(f"{self.team_binary_dir}/custom")
        team_dirs = [name for name in os.listdir(custom_dir)]
        path_list = []

        for path in team_dirs:
            path_list.append(f"{custom_dir}/{path}/start.sh")

        return path_list
    
    def get_team_path(self, base_dir, team_name):
        if self.is_binary_team(team_name):
            return f"{self.team_binary_dir}/{team_name}/start.sh"    
        else:
            return f"{base_dir}/{team_name}/{team_name.lower()}/src/start.sh" 

    def is_binary_team(self, team_name):
        # バイナリだけのチームなのか、ソースコードもあるチームなのかを判定する
        # TODO：HAMも実装するなら条件文に追加する
        if team_name == "HELIOS" or team_name == "HELIOS-Base":
            return False
        else:
            return True
    
    # エラー発生したため現在未使用
    # start.shまでのパスに-tオプションを必要なときに自動で追加する
    def add_teamname_option(self, team_path, visible_team_name):
        if visible_team_name is None:
            return team_path
        else:
            return f"{team_path} -t {visible_team_name}"

    def run_command(self, command):
        try:
            # shell=TrueはOSコマンドインジェクションの恐れがあるので要注意
            # 現状は各個人で使うので問題ないはず
            self.output_text = subprocess.run(command, check=True, text=True, shell=True, stdout=subprocess.PIPE).stdout
            print(self.output_text)
            print(f"実行が正常に終了しました: {command}\n\n")
        except subprocess.CalledProcessError as e:
            # コマンドがエラーを返した場合
            # TODO：エラー発生時はstderrをテキスト出力する
            print(e.stderr)
            print(f"コマンドにエラーが発生しました: {command}\n\n")
        except Exception as e:
            # その他の例外
            print(e.stderr)
            print(f"想定していないエラーが発生しました: {command}\n\n")

    def execute_matches(self, args):
        for left_team_path in self.left_team_path_list:
            for counter in range(args.match_number):
                # fixed_teamnameは指定しないと実行エラー吐くのでコメントアウト
                # 使う場合は必ずargparseのオプションのコメントアウトも解除すること
                execute_command = f"{args.base_dir}/tools/bin/rcssserver server::auto_mode = 1 " \
                                                                    f"server::synch_mode = {args.is_synch_mode} " \
                                                                    f"server::team_l_start = {left_team_path} " \
                                                                    f"server::team_r_start = {self.right_team_path} " \
                                                                    f"server::kick_off_wait = 50 " \
                                                                    f"server::half_time = 300 " \
                                                                    f"server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 " \
                                                                    f"server::penalty_shoot_outs = 0 " \
                                                                    f"server::game_logging = 1 server::text_logging = 1 " \
                                                                    f"server::game_log_dir = {self.log_dir} server::text_log_dir = {self.log_dir} "
                                                                    #f"server::fixed_teamname_l = {args.fixed_teamname_l} " \
                                                                    #f"server::fixed_teamname_r = {args.fixed_teamname_r} " \
                                                                    
            self.run_command(f"{execute_command}")
            self.output_log(counter)

    def output_log(self, counter):
        # pythonでは$HOMEをそのまま認識でないので、/home/ユーザ名 に置換
        log_dir = self.change_home_path(self.log_dir)

        # ファイル端末出力の内容を書き込む
        with open(f"{log_dir}/{self.formatted_date_time}_match{counter}.log", "w") as log_file:
            log_file.write(self.output_text)

    def change_home_path(self, target):
        return target.replace("$HOME", f"/home/{getpass.getuser()}") if "$HOME" in target else target

if __name__ == "__main__":
    main()