import subprocess
import argparse
import sys
import os
from datetime import datetime
import getpass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default=os.path.expandvars("$HOME/rcss"), 
                        help="Specify the base directory for environment setup")
    parser.add_argument("-l", "--left_team_name", dest="left_team_name", default="CYRUS", 
                        choices=["custom", "HELIOS2023", "helios-base", "yushan2023", "CYRUS",
                                 "EMPEROR", "Hermes2D", "Oxsy", "RoboCIn", "Damavand", "FRA-UNIted",
                                 "Hades2D", "ITAndorids", "The8"], help="Specify the left team name")
    parser.add_argument("-r", "--right_team_name", dest="right_team_name", default="HELIOS2023", 
                        choices=["custom", "HELIOS2023", "helios-base", "yushan2023", "CYRUS",
                                 "EMPEROR", "Hermes2D", "Oxsy", "RoboCIn", "Damavand", "FRA-UNIted",
                                 "Hades2D", "ITAndorids", "The8"], help="Specify the right team name")
    parser.add_argument("-n", "--match_number", dest="match_number", default=3, type=int, 
                        help="Specify the number of matches")
    parser.add_argument("--is_synch_mode", action="store_true", dest="is_synch_mode", help="Specify if synch mode should be enabled")
    
    args = parser.parse_args()
    auto_match = AutoMatch(args)
    auto_match.execute_matches(args)


class AutoMatch:
    def __init__(self, args):
        now = datetime.now()
        self.formatted_date_time = now.strftime("%Y%m%d%H%M%S")
        self.log_dir = args.base_dir + "/log_analysis/log/" + self.formatted_date_time
        self.team_binary_dir = args.base_dir + "/teams/rc2023"  # rc2023を追加
        self.left_team_path_list = []
        self.right_team_path_list = []
        self.output_text = None
        
        if args.left_team_name == "custom":
            self.left_team_path_list = self.get_custom_team_path_list()
        else:
            self.left_team_path_list.append(self.get_team_path(args.base_dir, args.left_team_name))

        if args.right_team_name == "custom":
            self.right_team_path_list = self.get_custom_team_path_list()
        else:
            self.right_team_path_list.append(self.get_team_path(args.base_dir, args.right_team_name))

    def get_custom_team_path_list(self):
        custom_dir = self.change_home_path(f"{self.team_binary_dir}/custom")
        team_dirs = [name for name in os.listdir(custom_dir)]
        path_list = []

        for path in team_dirs:
            path_list.append(f"{custom_dir}/{path}/start.sh")

        return path_list
    
    def get_team_path(self, base_dir, team_name):
        team_path_base = f"{self.team_binary_dir}/{team_name}"
        return f"{team_path_base}/start.sh"    

    def run_command(self, command):
        try:
            self.output_text = subprocess.run(command, check=True, text=True, shell=True, stdout=subprocess.PIPE).stdout
            print(self.output_text)
            print(f"Execution completed successfully: {command}\n\n")
        except subprocess.CalledProcessError as e:
            print(e.stderr)
            print(f"Error occurred with the command: {command}\n\n")
        except Exception as e:
            print(e.stderr)
            print(f"An unexpected error occurred: {command}\n\n")

    def execute_matches(self, args):
        for left_team_path in self.left_team_path_list:
            for right_team_path in self.right_team_path_list:
                for counter in range(args.match_number):
                    execute_command = f"{args.base_dir}/tools/bin/rcssserver server::auto_mode = 1 " \
                                      f"server::synch_mode = {args.is_synch_mode} " \
                                      f"server::team_l_start = {left_team_path} " \
                                      f"server::team_r_start = {right_team_path} " \
                                      f"server::kick_off_wait = 50 " \
                                      f"server::half_time = 300 " \
                                      f"server::nr_normal_halfs = 2 server::nr_extra_halfs = 0 " \
                                      f"server::penalty_shoot_outs = 0 " \
                                      f"server::game_logging = 1 server::text_logging = 1 " \
                                      f"server::game_log_dir = {self.log_dir} server::text_log_dir = {self.log_dir} "
                                                                            
                    self.run_command(f"{execute_command}")
                    self.output_log(counter, left_team_path, right_team_path)

    def output_log(self, counter, left_team_path, right_team_path):
        log_dir = self.change_home_path(self.log_dir)
        left_team_name, right_team_name = self.get_team_name(left_team_path, right_team_path)

        with open(f"{log_dir}/{self.formatted_date_time}_{left_team_name}_vs_{right_team_name}_match{counter}.log", "w") as log_file:
            log_file.write(self.output_text)

    def change_home_path(self, target):
        return target.replace("$HOME", f"/home/{getpass.getuser()}") if "$HOME" in target else target
    
    def get_team_name(self, left_team_path, right_team_path):
        if left_team_path.split("/")[-2] == "src":
            left_team_name = left_team_path.split("/")[-3]
        else:
            left_team_name = left_team_path.split("/")[-2]

        if right_team_path.split("/")[-2] == "src":
            right_team_name = right_team_path.split("/")[-3]
        else:
            right_team_name = right_team_path.split("/")[-2]

        return left_team_name, right_team_name
        

if __name__ == "__main__":
    main()
