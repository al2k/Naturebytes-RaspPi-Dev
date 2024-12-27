sudo apt update
sudo apt upgrade
sudo apt -y install python3-rpi.gpio python3-flask git imagemagick python3-opencv python3-arrow python3-picamera2

git clone https://github.com/naturebytes/Naturebytes-RaspPi-Dev.git
cp *.py /usr/local/src
cp -r static /usr/local/src
cp -r templates /usr/local/src
cp -r photos /usr/local/src