sudo apt update
sudo apt upgrade
sudo apt -y install python3-rpi.gpio python3-flask git imagemagic

cp *.py /usr/local/src
cp -r static /usr/local/src
cp -r templates /usr/local/src
cp -r photos /usr/local/src