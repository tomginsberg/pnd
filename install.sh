# print text in green "Installing pnd to your system ...
echo "\033[0;32mInstalling pnd to your system ...\033[0m"
# ask the user to select the install location default is /usr/local/bin
read -r -p "Enter the install location (please insure this location is in your system path) [/usr/local/bin]: " INSTALL_LOCATION
# if the user did not enter anything set the install location to /usr/local/bin
if [ -z "$INSTALL_LOCATION" ]; then
  INSTALL_LOCATION="/usr/local/bin"
fi
# download the file using wget
wget -O pnd https://raw.githubusercontent.com/tomginsberg/pnd/main/pnd.py
# ask the user for their python executable default is python3
read -r -p "Enter your python executable [python3]: " PYTHON_EXECUTABLE
# if the user did not enter anything set the python executable to python3
if [ -z "$PYTHON_EXECUTABLE" ]; then
  PYTHON_EXECUTABLE="python3"
fi
# prepend the python executable (#!PYTHON_EXECUTABLE) to the file named pnd.py and rename it pnd
echo "#!$PYTHON_EXECUTABLE" | cat - pnd >temp && mv temp pnd

# print moving the file to the install location
echo "Moving pnd executable to" $INSTALL_LOCATION
# move the file to the install location
sudo mv pnd $INSTALL_LOCATION
# make the file executable by the root user
echo "Setting permissions"
sudo chmod 700 $INSTALL_LOCATION/pnd

echo "Creating your secure data directory ~/.pnd"
echo "Passwords will be stored in ~/.pnd/data, readable only by the root user"
sudo mkdir -p ~/.pnd
sudo touch ~/.pnd/data
sudo chmod 700 ~/.pnd/data
echo " "
echo "\033[0;32mImprove the pnd user experience by adding the <pndc> function to your .bashrc/.zshrc file\033[0m"
# find out if the user is on mac or linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  # if the user is on linux then add the following line to the end of the .bashrc file
  echo "→ pndc directly copies the output of pnd to your clipboard for easy pasting and increased security"
  echo "✱ Note xclip must be installed (see https://github.com/astrand/xclip)"
  echo " "
  echo "pndc () {"
  echo "  sudo pnd \$1 | xclip"
  echo "}"
  echo " "
  echo '\033[0;32mFor beautiful fuzzy searching install fzf (https://github.com/junegunn/fzf) and add the <pnds> alias to your .bashrc/.zshrc file\033[0m'
  echo " "
  echo "alias pnds=\"sudo pnd ls | fzf | xargs sudo pnd | xclip\""
elif [[ "$OSTYPE" == "darwin"* ]]; then
  # if the user is on mac then add the following line to the end of the .bash_profile file
  echo "→ pndc directly copies the output of pnd to your clipboard for easy pasting and increased security"
  echo " "
  echo "pndc () {"
  echo "  sudo pnd \$1 | pbcopy"
  echo "}"
  # print a horizontal line
  echo " "
  echo '\033[0;32mFor beautiful fuzzy searching install fzf (https://github.com/junegunn/fzf) and add the <pnds> alias to your .bashrc/.zshrc file\033[0m'
  echo " "
  echo "alias pnds=\"sudo pnd ls | fzf | xargs sudo pnd | pbcopy\""
fi
echo " "
# print "Installation complete!" in green
echo "\033[0;32mInstallation complete!\033[0m"
echo "To get started run 'sudo pnd add'"
echo " "
# print in blue
# "Note: to use all the features of pnd please install python cryptography (pip install cryptography)"
echo "\033[0;34mNote: to use all the features of pnd please install python cryptography (pip install cryptography)\033[0m"
