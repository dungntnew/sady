#! /bin/sh
#
# install - install a sady program
# This comes from https://github.com/dungntnew/sady
#
# Copyright 2016 by the dungntew

# instruction
echo "=========================================================="
echo "                              "
echo "      INSTALL SADY - START -         "
echo "----------------------------------------------------------"

# install brew
if [ ! -x "$(command -v brew)" ]; then
  echo "[start install brew util command]"
  ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
  echo "[successfully installed] brew command"
fi

# install mplayer
if [ ! -x "$(command -v mplayer)" ]; then
  echo "[start install mplayer music command]"
  brew install mplayer
  echo "[successfully installed] mplayer command"
  which mplayer
fi

# install python3
if [ ! -x "$(command -v python3)" ]; then
  echo "[start install python3]"
  brew install python3
  echo "[successfully installed] python3"
  which python3
  echo "[start install virtualenv]"
  sudo pip3 install virtualenv
  echo "[successfully installed virtualenv]"
fi

# Clone & Install sady
SADY_HOME_DIR=~/.sady
git clone git@github.com:dungntnew/sady.git $SADY_HOME_DIR
cd $SADY_HOME_DIR
virtualenv -p python3 ./env && source ./env/bin/activate
pip install -r requirements.txt
echo "export SADY_HOME_DIR=$SADY_HOME_DIR" >> ~/.bash_profile
echo "alias sady='cd $SADY_HOME_DIR && ./env/bin/python3 ./__init__.py'" >> ~/.bash_profile
source ~/.bash_profile
echo "[successfully installed sady to $SADY_HOME_DIR"

echo "=========================================================="
echo "                              "
echo "      INSTALL SADY - END -         "
echo "----------------------------------------------------------"
echo "run: $ sady -q \"Lets it go Idina Menzel\" -> to enjoy (๑˃̵ᴗ˂̵) "



