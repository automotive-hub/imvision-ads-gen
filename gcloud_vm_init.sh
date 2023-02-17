sudo apt-get update
sudo apt-get install -y python
sudo apt-get install -y build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev

sudo apt full-upgrade

sudo apt-get install -y ffmpeg
sudo apt-get install -y xvfb
#

curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash - &&\
sudo apt-get install -y nodejs
#

npm config set unsafe-perm true
sudo npm i -g editly

sudo apt-get install -y python3-pip
# xvfb-run -s "-ac -screen 0 1280x1024x24" 