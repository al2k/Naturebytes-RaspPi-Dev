set -x
cp systemd/*.service /etc/systemd/system
chmod 644 /etc/systemd/system/camera.service
systemctl start camera.service
systemctl enable camera.service

chmod 644 /etc/systemd/system/web.service
systemctl start web.service
systemctl enable web.service

systemctl daemon-reload