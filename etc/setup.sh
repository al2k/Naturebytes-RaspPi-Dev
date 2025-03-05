sudo cp systemd/camera.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/camera.service
sudo systemctl start camera.service
sudo systemctl enable camera.service

sudo cp systemd/web.service /etc/systemd/system
sudo chmod 644 /etc/systemd/system/web.service
sudo systemctl start web.service
sudo systemctl enable web.service

sudo systemctl daemon-reload