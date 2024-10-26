sudo cp systemd/camera.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/camera.service
sudo systemctl start camera.service
sudo systemctl enable camera.service

sudo cp systemd/gallery.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/gallery.service
sudo systemctl start gallery.service
sudo systemctl enable gallery.service