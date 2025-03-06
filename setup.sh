set -x
if [$1]; then
sudo apt update
sudo apt upgrade
sudo apt -y install python3-rpi.gpio python3-flask git imagemagick
sudo apt -y install python3-opencv python3-arrow python3-picamera2
sudo apt -y install gunicorn3
fi

git clone https://github.com/naturebytes/Naturebytes-RaspPi-Dev.git
cd Naturebytes-RaspPi-Dev
sudo cp ./*.py /usr/local/src
sudo cp -r ./static /usr/local/src
sudo cp -r ./templates /usr/local/src
