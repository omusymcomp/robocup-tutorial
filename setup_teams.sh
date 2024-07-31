#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

BASE_DIR="$HOME/rcss"
HELIOS_BASE_DIR="${BASE_DIR}/teams/base_team"

# チームのインストール
cd ${BASE_DIR}
git clone git@github.com:omusymcomp/robocup_teams.git
mv robocup_teams teams

mkdir -p ${HELIOS_BASE_DIR}

# librcscのコンパイル(helios-base用)
cd ${HELIOS_BASE_DIR}
git clone git@github.com:helios-base/librcsc.git
cd librcsc
git checkout 348f41e
./bootstrap
./configure --prefix=${HELIOS_BASE_DIR}
make -j 4
make install

# helios-baseのコンパイル
cd ${HELIOS_BASE_DIR}
git clone -b develop git@github.com:helios-base/helios-base.git
cd helios-base
./bootstrap
./configure --with-librcsc=${HELIOS_BASE_DIR}
make -j 4
make install