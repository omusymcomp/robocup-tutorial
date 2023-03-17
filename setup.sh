#!/bin/bash

BASE_DIR="$HOME/rcss"
TOOLS_DIR="${BASE_DIR}/tools"
HELIOS_BASE_DIR="${BASE_DIR}/teams/base_team"
CONFIHURE_DIR="${BASE_DIR}/tools"

mkdir -p ${HELIOS_BASE_DIR}
mkdir -p ${CONFIHURE_DIR}


sudo apt-get install build-essential autoconf automake libtool 
sudo apt-get install flex bison libboost-all-dev 
sudo apt-get install libphonon-dev phonon-backend-gstreamer qt-sdk libaudio-dev 
sudo apt-get install libxt-dev libpng12-dev libglib2.0-dev libsm-dev libice-dev
sudo apt-get install libxi-dev libxrender-dev libfreetype6-dev libfontconfig1-dev
sudo apt install qtbase5-dev qttools5-dev-tools qt5-default

# librcscのコンパイル
cd ${TOOLS_DIR}
git clone git@github.com:helios-base/librcsc.git
cd librcsc
./bootstrap
./configure --prefix=${CONFIHURE_DIR}
make
make install

# soccerwindow2のコンパイル
cd ${TOOLS_DIR}
git clone git@github.com:helios-base/soccerwindow2.git
cd soccerwindow2
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make
make install

# fedit2のコンパイル
cd ${TOOLS_DIR}
git clone git@github.com:helios-base/fedit2.git
cd fedit2
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make
make install

# rcssserverのコンパイル
cd ${TOOLS_DIR}
git clone git@github.com:rcsoccersim/rcssserver.git
cd rcssserver
./bootstrap
./configure --prefix=${CONFIHURE_DIR}
make
make install

# rcssmonitorのコンパイル
cd ${TOOLS_DIR}
git clone git@github.com:rcsoccersim/rcssmonitor.git
cd rcssmonitor
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make
make install

# helios-baseのコンパイル
cd ${HELIOS_BASE_DIR}
git clone git@github.com:helios-base/helios-base.git
cd helios-base
./bootstrap
./configure --prefix=${CONFIHURE_DIR} --with-librcsc=${CONFIHURE_DIR}
make

