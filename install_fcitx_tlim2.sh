#!/bin/sh

GZ_FILE=tlim2.tar.gz
DATA_DIR=data1
FCITX_ROOT=/usr/share/fcitx

# Donwload and decompress
mkdir -p $DATA_DIR
if [ -f $DATA_DIR/$GZ_FILE ]
then
	echo "Skip download $GZ_FILE"
else
	echo "Download $GZ_FILE"
	wget -P $DATA_DIR http://language.moe.gov.tw/sujip/tlim2.tar.gz
	tar -C $DATA_DIR -xzvf $DATA_DIR/$GZ_FILE
fi

# convert binary file to text format
scim-make-table $DATA_DIR/tlim2.bin

# convert to fcitx files
./scim2fcitx.py -n tlim2 $DATA_DIR/tlim2.bin
txt2mb tlim2.txt tlim2.mb

# install
sudo apt-get install fcitx-table
sudo cp tlim2.conf $FCITX_ROOT/table/
sudo cp tlim2.mb $FCITX_ROOT/table/
sudo cp $DATA_DIR/tlim2.png $FCITX_ROOT/imicon/
