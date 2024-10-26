import logging
import subprocess

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("network")


def main():
    try:
        fyle = open("/media/pi/network.config")
    except FileExistsError:
        try:
            fyle = open('/boot/firmware/network.config')
        except FileExistsError:
            log.error("No network.config file found")
            return

        lines = fyle.readlines()
        ssid = password = None
        for line in lines:
            if 'ssid' in line:
                ssid = line.split(':')[1].strip()
            if 'password' in line:
                password = line.split(':')[1].strip()
        if ssid and password:
            command = f'nmcli device wifi con "{ssid}" password "{password}"'
            result = subprocess.run(command.split(), capture_output=True)
            log.info(result)
        else:
            log.error("Error: ssid and password not found in network.config")



if __name__ == "__main__":
    main()