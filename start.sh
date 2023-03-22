#!/bin/bash

#this file is made by kyo hatakeyama in 2021 to analyze rcss
#if there is already start.sh file, I chenged its name start0.sh
DIR=`dirname $0`

for i in {1..12} ; do
    $DIR/start localhost $DIR $i &
    sleep 0.3
done
