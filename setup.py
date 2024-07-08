import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--base_dir", dest="base_dir", default="$HOME/rcss", help="環境構築をするベースディレクトリを指定")    
    args = parser.parse_args()
    setup_tools = SetupTools(args)
    setup_tools.upgrade_packages()


class SetupTools:
    def __init__(self, args):
        self.base_dir = args.base_dir
        self.tools_dir = self.base_dir + "/tools"
        self.helios_base_dir = self.base_dir + "/teams/base_team"
        self.configure_dir = self.base_dir + "/tools"

    def upgrade_packages(self):
        self.run_command("sudo apt update -y")
        self.run_command("sudo apt upgrade -y")

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


#sudo apt update -y
#sudo apt upgrade -y
#
#BASE_DIR="$HOME/rcss"
#TOOLS_DIR="${BASE_DIR}/tools"
#HELIOS_BASE_DIR="${BASE_DIR}/teams/base_team"
#CONFIHURE_DIR="${BASE_DIR}/tools"
#
#mkdir -p ${HELIOS_BASE_DIR}
#mkdir -p ${CONFIHURE_DIR}
#
## 実行に必要なパッケージのインストール
#sudo apt-get install build-essential autoconf automake libtool 
#sudo apt-get install flex bison libboost-all-dev 
##sudo apt-get install libphonon-dev phonon-backend-gstreamer qt-sdk libaudio-dev 
#sudo apt-get install libxt-dev libglib2.0-dev libsm-dev libice-dev
#sudo apt-get install libxi-dev libxrender-dev libfreetype6-dev libfontconfig1-dev
##sudo apt install qtbase5-dev qttools5-dev-tools qt5-default
#sudo apt install qtbase5-dev qt5-qmake
#
#
## 環境変数の追加
##実行ごとに追記されるので要注意
#echo 'export LD_LIBRARY_PATH=$HOME/rcss/tools/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
#echo 'export PATH=$HOME/rcss/tools/bin:$PATH' >> ~/.profile
##echo 'export RCSSMONITOR=sswindow2' >> ~/.bashrc
#
#
## librcscのコンパイル
#cd ${TOOLS_DIR}
#git clone -b develop git@github.com:helios-base/librcsc.git
#cd librcsc
#./bootstrap
#./configure --prefix=${CONFIHURE_DIR}
#make
#make install
#
## soccerwindow2のコンパイル
#cd ${TOOLS_DIR}
#git clone -b develop git@github.com:helios-base/soccerwindow2.git
#cd soccerwindow2
#./bootstrap
#./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
#make
#make install
#
## fedit2のコンパイル
#cd ${TOOLS_DIR}
#git clone -b develop git@github.com:helios-base/fedit2.git
#cd fedit2
#./bootstrap
#./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
#make
#make install
#
## rcssserverのコンパイル
#cd ${TOOLS_DIR}
#git clone -b develop git@github.com:rcsoccersim/rcssserver.git
#cd rcssserver
#./bootstrap
#./configure --prefix=${CONFIHURE_DIR}
#make
#make install
#
## rcssmonitorのコンパイル
#cd ${TOOLS_DIR}
#git clone -b develop git@github.com:rcsoccersim/rcssmonitor.git
#cd rcssmonitor
#./bootstrap
#./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
#make
#make install
#
## helios-baseのコンパイル
#cd ${HELIOS_BASE_DIR}
#git clone -b develop git@github.com:helios-base/helios-base.git
#cd helios-base
#./bootstrap
#./configure --with-librcsc=${CONFIHURE_DIR}
#make



if __name__ == "__main__":
    main()