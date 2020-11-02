#!/bin/bash
#title           :install_libs.bash
#description     :This script will install all the needed libraries for the
#                 BAGPIPES SED-fitting code on the Linux Debian 9 on the
#                 Google cloude computing instances
#author		       :Abtin Shahidi
#date            :06/28/2019
#version         :0.1
#usage		       : sudo bash install_libs.bash
#notes           : It does not have any error handling procedure and it has
#                : written to work on the particular machine mentioned.
#bash_version    :4.1.5(1)-release
#=======================================


# installing essential libraries before building python 3.7
sudo apt-get --assume-yes install build-essential cmake checkinstall
sudo apt-get --assume-yes install libreadline-gplv2-dev libncursesw5-dev
sudo apt-get --assume-yes install libssl-dev  libsqlite3-dev tk-dev libgdbm-dev
sudo apt-get --assume-yes install libc6-dev libbz2-dev libffi-dev zlib1g-dev

# Download and install python3.7.3 from the source file
mkdir src
cd src/
# Downloading
sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz
sudo tar xzf Python-3.7.3.tgz
cd Python-3.7.3
# installing
sudo ./configure --enable-optimizations
sudo make altinstall


# Installing the required libraries for PyMultiNest via pip
sudo pip3.7 install numpy scipy matplotlib

# Installing fortran and needed libraries for MultiNest
sudo apt-get --assume-yes install libblas3 liblapack3 liblapack-dev libblas-dev
sudo apt-get --assume-yes install gfortran


# Installing git
sudo apt-get --assume-yes install git
git config --global user.name "user@VM"
git config --global user.email "user@user.user"


# Download and install MultiNest, point to the directory
cd /home/user/src/
git clone https://github.com/JohannesBuchner/MultiNest.git
cd MultiNest/build/
cmake .. && make

export LD_LIBRARY_PATH=/home/user/src/MultiNest
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
export LD_LIBRARY_PATH=/home/user/src/MultiNest/lib/:$LD_LIBRARY_PATH


sudo ldconfig /home/user/src/MultiNest/lib/
# Download and install PyMultiNest
git clone https://github.com/JohannesBuchner/PyMultiNest.git

cd PyMultiNest/
# Installing
sudo python3.7 setup.py install
export PATH=$PATH:/home/user/.local/bin/

# install the BAGPIPES
sudo pip3.7 install bagpipes --user
# Check if importing BAGPIPES was successful
sudo python3.7 -c "import bagpipes"
