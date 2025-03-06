set -x
sudo apt update
sudo apt upgrade -y
sudo apt -y install python3-rpi.gpio python3-flask git imagemagick
sudo apt -y install python3-opencv python3-arrow python3-picamera2
sudo apt -y install gunicorn3

# Install BTBerryWifi
curl  -L https://raw.githubusercontent.com/nksan/Rpi-SetWiFi-viaBluetooth/main/btwifisetInstall.sh | bash

git clone https://github.com/naturebytes/Naturebytes-RaspPi-Dev.git
cd Naturebytes-RaspPi-Dev

sudo cp systemd/*.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/camera.service
sudo systemctl start camera.service
sudo systemctl enable camera.service

sudo chmod 644 /etc/systemd/system/web.service
sudo systemctl start web.service
sudo systemctl enable web.service

sudo systemctl daemon-reload