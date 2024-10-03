import subprocess
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default=os.path.expandvars("$HOME/rcss"), help="Specify the base directory for environment setup")
    parser.add_argument("-t", "--install_target", dest="install_target", default="minisetup", 
                        choices=["all", "minisetup", "tools", "librcsc", "rcssserver", "soccerwindow2", 
                                 "rcssmonitor", "fedit2", "helios_base", "helios", "loganalyzer3"], 
                        help="Specify the installation target. 'all' installs everything, 'minisetup' installs the minimal setup required for execution, and specific tools or teams are installed if specified.")
    parser.add_argument("-j", "--jobs", type=int, dest="jobs", help="Specify the number of jobs to run simultaneously during compilation (make -j option)")
    parser.add_argument("--upgrade_packages", action="store_true", dest="upgrade_packages", help="Specify if package updates should be performed before compiling")
    parser.add_argument("--is_installation_of_essential_packages", action="store_true", dest="is_installation_of_essential_packages", 
                        help="Specify if essential packages should be installed before compilation")
    parser.add_argument("--add_environment_variable", action="store_true", dest="add_environment_variable", help="Specify if environment variables should be added. Required during the initial setup.")
    args = parser.parse_args()


    setup_tools = SetupTools(args)
    setup_teams = SetupTeams(args)
    if args.upgrade_packages:
        setup_tools.upgrade_packages()
    
    if args.is_installation_of_essential_packages:
        setup_tools.install_essential_packages()

    if args.add_environment_variable:
        setup_tools.add_environment_variables()

    if args.install_target == "all":
        setup_tools.install_librcsc()
        setup_tools.install_rcssserver()
        setup_tools.install_soccerwindow2()
        setup_tools.install_rcssmonitor()
        setup_tools.install_fedit2()
        setup_tools.install_loganalyzer3()
        setup_teams.install_teams()
        setup_teams.install_helios_base()
        setup_teams.replace_username()
        setup_teams.add_execution_permission()
    elif args.install_target == "minisetup":
        setup_tools.install_librcsc()
        setup_tools.install_rcssserver()
        setup_tools.install_soccerwindow2()
        setup_teams.install_helios_base()
    elif args.install_target == "tools":
        setup_tools.install_librcsc()
        setup_tools.install_rcssserver()
        setup_tools.install_soccerwindow2()
        setup_tools.install_rcssmonitor()
        setup_tools.install_fedit2()
        setup_tools.install_loganalyzer3()
    else:
        called_method = getattr(setup_tools, f"install_{args.install_target}")
        called_method()

class SetupTools:
    def __init__(self, args):
        self.base_dir = args.base_dir
        self.tools_dir = self.base_dir + "/tools"
        self.configure_dir = self.base_dir + "/tools"
        self.jobs = args.jobs
        self.make_command = "make"
        if self.jobs:
            self.make_command += f" -j {self.jobs}"

    def run_command(self, command):
        try:
            # Be careful with shell=True, as it can lead to OS command injection
            # Since this is currently used for personal purposes, it shouldn't be an issue
            result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
            print(result.stdout)
            print(f"Execution completed successfully: {command}\n\n")
        except subprocess.CalledProcessError as e:
            # When the command returns an error
            print(e.stderr)
            print(f"An error occurred with the command: {command}\n\n")
        except Exception as e:
            # Other exceptions
            print(e.stderr)
            print(f"An unexpected error occurred: {command}\n\n")

    def upgrade_packages(self):
        self.run_command("sudo apt update -y")
        self.run_command("sudo apt upgrade -y")

    def install_essential_packages(self):
        # Install the essential packages for execution
        self.run_command("sudo apt-get install build-essential autoconf automake libtool")
        self.run_command("sudo apt-get install flex bison libboost-all-dev")
        self.run_command("sudo apt-get install libphonon-dev phonon-backend-gstreamer qt-sdk libaudio-dev")
        self.run_command("sudo apt-get install libxt-dev libglib2.0-dev libsm-dev libice-dev")
        self.run_command("sudo apt-get install libxi-dev libxrender-dev libfreetype6-dev libfontconfig1-dev")
        self.run_command("sudo apt install qtbase5-dev qttools5-dev-tools qt5-default")
        self.run_command("sudo apt install qtbase5-dev qt5-qmake")

    def add_environment_variables(self):
        # Add environment variables
        # Note that this appends with each function call
        self.run_command("echo 'export LD_LIBRARY_PATH=$HOME/rcss/tools/lib:$LD_LIBRARY_PATH' >> ~/.bashrc")
        self.run_command("echo 'export PATH=$HOME/rcss/tools/bin:$PATH' >> ~/.profile")
        self.run_command("echo 'export RCSSMONITOR=sswindow2' >> ~/.bashrc")

    def install_librcsc(self):
        # Compile librcsc
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/librcsc"):
            self.run_command("git clone -b develop https://github.com/helios-base/librcsc.git")
        else:
            print(f"{self.tools_dir}"+"/librcsc exists, skipping git clone")
        os.chdir(f"./librcsc")
        self.run_command(f"{self.tools_dir}/librcsc/bootstrap")
        self.run_command(f"{self.tools_dir}/librcsc/configure --prefix={self.configure_dir}")
        self.run_command(self.make_command)
        self.run_command(f"make install")

    def install_rcssserver(self):
        # Compile rcssserver
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/rcssserver"):
            self.run_command("git clone -b develop https://github.com/rcsoccersim/rcssserver.git")
        else:
            print(f"{self.tools_dir}"+"/rcssserver exists, skipping git clone")
        os.chdir(f"./rcssserver")
        self.run_command(f"{self.tools_dir}/rcssserver/bootstrap")
        self.run_command(f"{self.tools_dir}/rcssserver/configure --prefix={self.configure_dir}")
        self.run_command(self.make_command)
        self.run_command(f"make install")

    def install_soccerwindow2(self):
        # Compile soccerwindow2
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/soccerwindow2"):
            self.run_command("git clone -b develop https://github.com/helios-base/soccerwindow2.git")
        else:
            print(f"{self.tools_dir}"+"/soccerwindow2 exists, skipping git clone")
        os.chdir(f"./soccerwindow2")
        self.run_command(f"{self.tools_dir}/soccerwindow2/bootstrap")
        self.run_command(f"{self.tools_dir}/soccerwindow2/configure --prefix={self.configure_dir} --with-librcsc={self.configure_dir}")
        self.run_command(self.make_command)
        self.run_command(f"make install")

    def install_rcssmonitor(self):
        # Compile rcssmonitor
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/rcssmonitor"):
            self.run_command("git clone -b develop https://github.com/rcsoccersim/rcssmonitor.git")
        else:
            print(f"{self.tools_dir}"+"/rcssmonitor exists, skipping git clone")
        os.chdir(f"./rcssmonitor")
        self.run_command(f"{self.tools_dir}/rcssmonitor/bootstrap")
        self.run_command(f"{self.tools_dir}/rcssmonitor/configure --prefix={self.configure_dir} --with-librcsc={self.configure_dir}")
        self.run_command(self.make_command)
        self.run_command(f"make install")

    def install_fedit2(self):
        # Compile fedit2
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/fedit2"):
            self.run_command("git clone -b develop https://github.com/helios-base/fedit2.git")
        else:
            print(f"{self.tools_dir}"+"/fedit2 exists, skipping git clone")
        os.chdir(f"./fedit2")
        self.run_command(f"{self.tools_dir}/fedit2/bootstrap")
        self.run_command(f"{self.tools_dir}/fedit2/configure --prefix={self.configure_dir} --with-librcsc={self.configure_dir}")
        self.run_command(self.make_command)
        self.run_command(f"make install")
    
    def install_loganalyzer3(self):
        # Compile loganalyzer3
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/loganalyzer3"):
            self.run_command("git clone https://github.com/opusymcomp/loganalyzer3.git")
        else:
            print(f"{self.tools_dir}"+"/loganalyzer3 exists, skipping git clone")

class SetupTeams:
    def __init__(self, args):
        # Dynamically get the username of the executor and construct the path
        username = os.getlogin()
        self.base_dir = args.base_dir
        self.teams_dir = self.base_dir + "/teams"
        self.user_teams_dir = f"/home/{username}/rcss/teams"
        self.base_team_dir = self.base_dir + "/teams/base_team"
        self.configure_dir = self.base_dir + "/teams/base_team"
        self.jobs = args.jobs
        self.make_command = "make"
        if self.jobs:
            self.make_command += f" -j {self.jobs}"

    def run_command(self, command):
        try:
            # Be careful with shell=True, as it can lead to OS command injection
            # Since this is currently used for personal purposes, it shouldn't be an issue
            result = subprocess.run(command, check=True, text=True, capture_output=True, shell=True)
            print(result.stdout)
            print(f"Execution completed successfully: {command}\n")
        except subprocess.CalledProcessError as e:
            # When the command returns an error
            print(e.stderr)
            print(f"An error occurred with the command: {command}\n\n")
        except Exception as e:
            # Other exceptions
            print(e.stderr)
            print(f"An unexpected error occurred: {command}\n\n")    

    def install_teams(self):
        self.run_command(f"mkdir -p {self.base_dir}")
        os.chdir(f"{self. base_dir}")
        if not os.path.exists(f"{self.teams_dir}"):
            self.run_command("git clone https://github.com/omusymcomp/robocup_teams.git teams")
        else:
            print(f"{self.teams_dir} exists, skipping git clone")   

    def install_librcsc_for_helios_base(self):
        # Compile librcsc
        self.run_command(f"mkdir -p {self.base_team_dir}")
        os.chdir(f"{self.base_team_dir}")
        if not os.path.exists(self.base_team_dir+"/librcsc"):
            self.run_command("git clone -b develop https://github.com/helios-base/librcsc.git")
        else:
            print(f"{self.base_team_dir}"+"/librcsc exists, skipping git clone")
        os.chdir(f"./librcsc")
        self.run_command(f"make distclean")
        self.run_command(f"git checkout 348f41e")
        self.run_command(f"{self.configure_dir}/librcsc/bootstrap")
        self.run_command(f"{self.configure_dir}/librcsc/configure --prefix={self.configure_dir}")
        self.run_command(self.make_command)
        self.run_command(f"make install")  
    
    def install_helios_base(self):
        self.run_command(f"mkdir -p {self.base_team_dir}")
        # Compile librcsc for HELIOS-Base
        self.install_librcsc_for_helios_base()
        # Compile HELIOS-Base
        os.chdir(f"{self.base_team_dir}")
        if not os.path.exists(self.base_team_dir+"/helios-base"):
            self.run_command("git clone -b develop https://github.com/helios-base/helios-base.git")
        else:
            print(f"{self.base_team_dir}"+"/helios-base exists, skipping git clone")
        os.chdir(f"./helios-base")
        self.run_command(f"{self.configure_dir}/helios-base/bootstrap")
        self.run_command(f"{self.configure_dir}/helios-base/configure --with-librcsc={self.configure_dir}")
        self.run_command(self.make_command)

    def replace_username(self):
        # Get the username of the executor
        username = os.getlogin()
        directory = self.user_teams_dir
        try:
            if not os.path.exists(directory):
                print(f"The specified directory does not exist: {directory}")
                return

            # Process all files in the specified directory
            for root, dirs, files in os.walk(directory):
                # Skip the .git directory
                if '.git' in dirs:
                    dirs.remove('.git')

                for file in files:
                    # Open target files as text
                    file_path = os.path.join(root, file)
                    
                    # Read file content
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    # Replace "username" with the executor's username
                    updated_content = content.replace('/home/username/', f'/home/{username}/')

                    # Overwrite the file with the updated content
                    with open(file_path, 'w') as f:
                        f.write(updated_content)

            print("Path replacement within files has been completed")
        
        except Exception as e:
            # Other exceptions
            print(str(e))
            print("An unexpected error occurred") 

    def add_execution_permission(self):
        directory = self.user_teams_dir
        for root, dirs, files in os.walk(directory):
            for file in files:
                # Add execution permission based on script file extension or specific filenames
                if file.endswith('.sh') or 'start' in file:
                    file_path = os.path.join(root, file)
                    self.run_command(f"chmod +x {file_path}")

if __name__ == "__main__":
    main()