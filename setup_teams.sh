#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

BASE_DIR="$HOME/rcss"
HAM_DIR="${BASE_DIR}/HAM"
HELIOS_DIR="${BASE_DIR}/HELIOS"

mkdir -p ${HAM_DIR}
mkdir -p ${HELIOS_DIR}

## librcscのコンパイル(HAM用)
cd ${HAM_DIR}
git clone git@github.com:helios-base/librcsc.git
cd librcsc
git checkout 4c45970
./bootstrap
./configure --prefix=${HAM_DIR}
make
make install

# HAMのコンパイル
cd ${HAM_DIR}
git clone git@github.com:omusymcomp/omuHam.git
cd omuHam
git checkout develop
chmod 744 tensorflow_c++_install.sh
# ubuntu22だとpythonコマンドがデフォルトでないので必須
sudo apt install python-is-python3
# 高負荷が長時間かかるため要注意
./tensorflow_c++_install.sh
./bootstrap
./configure --with-librcsc=${HAM_DIR}
make




# librcscのコンパイル(HELIOS用)
cd ${HELIOS_DIR}
git clone git@github.com:helios-base/librcsc.git
cd librcsc
git checkout develop
./bootstrap
./configure --prefix=${HELIOS_DIR}
make
make install

# HELIOSのコンパイル
cd ${HELIOS_DIR}
git clone git@github.com:helios-base/helios.git
cd helios
git checkout develop
./bootstrap
./configure --prefix=${HELIOS_DIR} --with-librcsc=${HELIOS_DIR}
make