#!/bin/bash

sudo apt update -y
sudo apt upgrade -y

BASE_DIR="$HOME/rcss"
HELIOS_DIR="${BASE_DIR}/HELIOS"
HELIOS_BASE_DIR="${BASE_DIR}/teams/base_team"
CONFIGURE_DIR="${BASE_DIR}/tools"

mkdir -p ${HELIOS_DIR}
mkdir -p ${HELIOS_BASE_DIR}

## librcscのコンパイル(HAM用)
cd ${HAM_DIR}
git clone git@github.com:helios-base/librcsc.git
cd librcsc
git checkout 4c45970
./bootstrap
./configure --prefix=${HAM_DIR}
make -j 4
make install

# librcscのコンパイル(HELIOS用)
cd ${HELIOS_DIR}
git clone git@github.com:helios-base/librcsc.git
cd librcsc
git checkout develop
./bootstrap
./configure --prefix=${HELIOS_DIR}
make -j 4
make install

# HELIOSのコンパイル
cd ${HELIOS_DIR}
git clone git@github.com:helios-base/helios.git
cd helios
git checkout develop
./bootstrap
./configure --prefix=${HELIOS_DIR} --with-librcsc=${HELIOS_DIR}
make -j 4
make install


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