#!/bin/bash

sudo apt-get update

sudo apt-get install git vim python-pip python-virtualenv build-essential python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev

virtualenv fshare

fshare/bin/pip install -r requirements.txt

git clone git://github.com/amix/vimrc.git ~/.vim_runtime
sh ~/.vim_runtime/install_basic_vimrc.sh

echo "Done"

