# Ubunto LTS CPU intensive
sudo apt-get update
sudo apt-get install -y python
sudo apt-get install -y build-essential libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev


# sudo apt-get install -y build-essential libxi-dev libglu1-mesa-dev libglew-dev pkg-config
# sudo apt-get install -y python-is-python3
sudo add-apt-repository -y ppa:savoury1/ffmpeg4
sudo add-apt-repository -y ppa:savoury1/graphics
sudo add-apt-repository -y ppa:savoury1/multimedia
sudo apt-get update -y

sudo apt-get install -y ffmpeg
sudo apt-get install -y xvfb
#

curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash - &&\
sudo apt-get install -y nodejs
#

sudo npm config set unsafe-perm true
sudo npm i -g editly
sudo npm i -g pm2

sudo apt-get install -y python3-pip
#
pip3 install -r requirements.txt

# sudo -v ; curl https://rclone.org/install.sh | sudo bash
# xvfb-run -s "-ac -screen 0 1280x1024x24" 