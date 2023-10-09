#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

BASE_DIR="$HOME/rcss"
TOOLS_DIR="${BASE_DIR}/tools"
HELIOS_BASE_DIR="${BASE_DIR}/teams/base_team"
CONFIHURE_DIR="${BASE_DIR}/tools"

mkdir -p ${HELIOS_BASE_DIR}
mkdir -p ${CONFIHURE_DIR}

# 実行に必要なパッケージのインストール
sudo apt-get install build-essential autoconf automake libtool 
sudo apt-get install flex bison libboost-all-dev 
#sudo apt-get install libphonon-dev phonon-backend-gstreamer qt-sdk libaudio-dev 
sudo apt-get install libxt-dev libglib2.0-dev libsm-dev libice-dev
sudo apt-get install libxi-dev libxrender-dev libfreetype6-dev libfontconfig1-dev
#sudo apt install qtbase5-dev qttools5-dev-tools qt5-default
sudo apt install qtbase5-dev qt5-qmake


# 環境変数の追加
#実行ごとに追記されるので要注意
echo 'export LD_LIBRARY_PATH=$HOME/rcss/tools/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PATH=$HOME/rcss/tools/bin:$PATH' >> ~/.profile
#echo 'export RCSSMONITOR=sswindow2' >> ~/.bashrc


# librcscのコンパイル
cd ${TOOLS_DIR}
git clone -b develop git@github.com:helios-base/librcsc.git
cd librcsc
./bootstrap
./configure --prefix=${CONFIHURE_DIR}
make
make install

# soccerwindow2のコンパイル
cd ${TOOLS_DIR}
git clone -b develop git@github.com:helios-base/soccerwindow2.git
cd soccerwindow2
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make
make install

# fedit2のコンパイル
cd ${TOOLS_DIR}
git clone -b develop git@github.com:helios-base/fedit2.git
cd fedit2
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make
make install

# rcssserverのコンパイル
cd ${TOOLS_DIR}
git clone -b develop git@github.com:rcsoccersim/rcssserver.git
cd rcssserver
./bootstrap
./configure --prefix=${CONFIHURE_DIR}
make
make install

# rcssmonitorのコンパイル
cd ${TOOLS_DIR}
git clone -b develop git@github.com:rcsoccersim/rcssmonitor.git
cd rcssmonitor
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make
make install

# helios-baseのコンパイル
cd ${HELIOS_BASE_DIR}
git clone -b develop git@github.com:helios-base/helios-base.git
cd helios-base
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make

