# robocup-tutorial

### 各ファイルの簡単な説明 ###
* setup.sh：robocup実行に必要なライブラリ、ツールなどを一括でコンパイルまで行う。具体的には以下のソースが該当する
    * librcsc
    * soccerwindow2
    * fedit2
    * rcssserver
    * rcssmonitor
    * helios-base
* setup.sh：OMU-HAM、HELIOSを自動でコンパイルまで行う
* start.sh：デフォルトのスクリプトでは動かないバイナリに利用する
* fixed_teams_autogame.sh：特定のチームの試合実行を任意の回数だけ行う