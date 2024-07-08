import subprocess
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="$HOME/rcss", help="環境構築をするベースディレクトリを指定")
    parser.add_argument("-t", "--install_target", dest="install_target", default="minisetup", 
                        choices=["all", "minisetup", "tools", "librcsc", "rcssserver", "soccerwindow2", 
                                 "rcssmonitor", "fedit2", "helios_base", "helios"], 
                        help="インストールする対象を指定する。allはすべて、minisetupは実行に必要な最小構成、それ以外の場合は指定した名前のツール・チームをインストールする")
    parser.add_argument("--upgrade_packages", action="store_true", dest="upgrade_packages", help="コンパイル実行前にパッケージアップデートをする場合は指定する")
    parser.add_argument("--is_installation_of_essential_packages", action="store_true", dest="is_installation_of_essential_packages", 
                        help="コンパイル実行前にパッケージアップデートをする場合は指定する")
    parser.add_argument("--add_environment_variable", action="store_true", dest="add_environment_variable", help="環境変数を追加する場合は指定する。初回セットアップ時は必須")
    args = parser.parse_args()


    setup_tools = SetupTools(args)
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
        setup_tools.install_helios_base()
    elif args.install_target == "minisetup":
        setup_tools.install_librcsc()
        setup_tools.install_rcssserver()
        setup_tools.install_soccerwindow2()
        setup_tools.install_helios_base()
    elif args.install_target == "tools":
        setup_tools.install_librcsc()
        setup_tools.install_rcssserver()
        setup_tools.install_soccerwindow2()
        setup_tools.install_rcssmonitor()
        setup_tools.install_fedit2()
    else:
        called_method = getattr(setup_tools, f"install_{args.install_target}")
        called_method()


class SetupTools:
    def __init__(self, args):
        self.base_dir = args.base_dir
        self.tools_dir = self.base_dir + "/tools"
        self.helios_base_dir = self.base_dir + "/HELIOS-Base"
        self.helios_dir = self.base_dir + "/HELIOS"
        self.configure_dir = self.base_dir + "/tools"

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

    def upgrade_packages(self):
        self.run_command("sudo apt update -y")
        self.run_command("sudo apt upgrade -y")

    def install_essential_packages(self):
        # 実行に必要なパッケージのインストール
        self.run_command("sudo apt-get install build-essential autoconf automake libtool")
        self.run_command("sudo apt-get install flex bison libboost-all-dev")
        self.run_command("sudo apt-get install libphonon-dev phonon-backend-gstreamer qt-sdk libaudio-dev")
        self.run_command("sudo apt-get install libxt-dev libglib2.0-dev libsm-dev libice-dev")
        self.run_command("sudo apt-get install libxi-dev libxrender-dev libfreetype6-dev libfontconfig1-dev")
        self.run_command("sudo apt install qtbase5-dev qttools5-dev-tools qt5-default")
        self.run_command("sudo apt install qtbase5-dev qt5-qmake")

    def add_environment_variables(self):
        # 環境変数の追加
        # 関数呼び出しごとに追記されるので要注意
        self.run_command("echo 'export LD_LIBRARY_PATH=$HOME/rcss/tools/lib:$LD_LIBRARY_PATH' >> ~/.bashrc")
        self.run_command("echo 'export PATH=$HOME/rcss/tools/bin:$PATH' >> ~/.profile")
        self.run_command("echo 'export RCSSMONITOR=sswindow2' >> ~/.bashrc")

    def install_librcsc(self):
        # librcscのコンパイル
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/librcsc"):
            self.run_command("git clone -b develop git@github.com:helios-base/librcsc.git")
        else:
            print(f"{self.tools_dir}"+"/librcsc が存在するため、git cloneをスキップします")
        os.chdir(f"./librcsc")
        self.run_command(f"{self.tools_dir}/librcsc/bootstrap")
        self.run_command(f"{self.tools_dir}/librcsc/configure --prefix={self.configure_dir}")
        self.run_command(f"make")
        self.run_command(f"make install")

    def install_librcsc_for_helios_base(self):
        # librcscのコンパイル
        # HELIOS-Base用librcscは、$HOME/rcss/HELIOS-Baseにある想定
        self.run_command(f"mkdir -p {self.helios_base_dir}")
        os.chdir(f"{self.helios_base_dir}")
        if not os.path.exists(self.helios_base_dir+"/librcsc"):
            self.run_command("git clone -b master git@github.com:helios-base/librcsc.git")
        else:
            print(f"{self.helios_base_dir}"+"/librcsc が存在するため、git cloneをスキップします")
        os.chdir(f"./librcsc")
        self.run_command(f"{self.helios_base_dir}/librcsc/bootstrap")
        self.run_command(f"{self.helios_base_dir}/librcsc/configure --prefix={self.helios_base_dir}")
        self.run_command(f"make")
        self.run_command(f"make install")

    def install_rcssserver(self):
        # rcssserverのコンパイル
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/rcssserver"):
            self.run_command("git clone -b develop git@github.com:rcsoccersim/rcssserver.git")
        else:
            print(f"{self.tools_dir}"+"/rcssserver が存在するため、git cloneをスキップします")
        os.chdir(f"./rcssserver")
        self.run_command(f"{self.tools_dir}/rcssserver/bootstrap")
        self.run_command(f"{self.tools_dir}/rcssserver/configure --prefix={self.configure_dir}")
        self.run_command(f"make")
        self.run_command(f"make install")

    def install_soccerwindow2(self):
        # soccerwindow2のコンパイル
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/soccerwindow2"):
            self.run_command("git clone -b develop git@github.com:helios-base/soccerwindow2.git")
        else:
            print(f"{self.tools_dir}"+"/soccerwindow2 が存在するため、git cloneをスキップします")
        os.chdir(f"./soccerwindow2")
        self.run_command(f"{self.tools_dir}/soccerwindow2/bootstrap")
        self.run_command(f"{self.tools_dir}/soccerwindow2/configure --prefix={self.configure_dir} --with-librcsc={self.configure_dir}")
        self.run_command(f"make")
        self.run_command(f"make install")

    def install_rcssmonitor(self):
        # rcssmonitorのコンパイル
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/rcssmonitor"):
            self.run_command("git clone -b develop git@github.com:rcsoccersim/rcssmonitor.git")
        else:
            print(f"{self.tools_dir}"+"/rcssmonitor が存在するため、git cloneをスキップします")
        os.chdir(f"./rcssmonitor")
        self.run_command(f"{self.tools_dir}/rcssmonitor/bootstrap")
        self.run_command(f"{self.tools_dir}/rcssmonitor/configure --prefix={self.configure_dir} --with-librcsc={self.configure_dir}")
        self.run_command(f"make")
        self.run_command(f"make install")

    def install_fedit2(self):
        # fedit2のコンパイル
        self.run_command(f"mkdir -p {self.configure_dir}")
        os.chdir(f"{self.tools_dir}")
        if not os.path.exists(self.tools_dir+"/fedit2"):
            self.run_command("git clone -b develop git@github.com:helios-base/fedit2.git")
        else:
            print(f"{self.tools_dir}"+"/fedit2 が存在するため、git cloneをスキップします")
        os.chdir(f"./fedit2")
        self.run_command(f"{self.tools_dir}/fedit2/bootstrap")
        self.run_command(f"{self.tools_dir}/fedit2/configure --prefix={self.configure_dir} --with-librcsc={self.configure_dir}")
        self.run_command(f"make")
        self.run_command(f"make install")

    def install_helios_base(self):
        self.run_command(f"mkdir -p {self.helios_base_dir}")
        # HELIOS-Base用のlibrcscのコンパイル
        self.install_librcsc_for_helios_base()
        # HELIOS-Baseのコンパイル
        os.chdir(f"{self.helios_base_dir}")
        if not os.path.exists(self.helios_base_dir+"/helios-base"):
            self.run_command("git clone -b develop git@github.com:helios-base/helios-base.git")
        else:
            print(f"{self.helios_base_dir}"+"/helios-base が存在するため、git cloneをスキップします")
        os.chdir(f"./helios-base")
        self.run_command(f"{self.helios_base_dir}/helios-base/bootstrap")
        self.run_command(f"{self.helios_base_dir}/helios-base/configure --with-librcsc={self.helios_base_dir}")
        self.run_command(f"make")

    def install_helios(self):
        pass


if __name__ == "__main__":
    main()