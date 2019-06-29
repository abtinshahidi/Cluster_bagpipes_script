#!/bin/bash
#title           :mount_data.bash
#description     :This script will install all the needed libraries for the
#                 gcsfuse in order to mount google cloud storage the bucket
#author		       :Abtin Shahidi
#date            :06/28/2019
#version         :0.1
#usage		       : sudo bash mount_data.bash
#notes           : ------
#bash_version    :4.1.5(1)-release
#=======================================

export GCSFUSE_REPO=gcsfuse-`lsb_release -c -s`
echo "deb http://packages.cloud.google.com/apt $GCSFUSE_REPO main" | sudo tee /etc/apt/sources.list.d/gcsfuse.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --assume-yes add -


sudo apt-get --assume-yes update
sudo apt-get --assume-yes install gcsfuse

sudo groupadd fuse
sudo usermod -a -G fuse $USER
exit
