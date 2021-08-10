# modem check and reboot

Modem Bandwidth Test and Reboot (still deciding on a name)

Author: ZyMOS
Date: 06/2021
License: GPLv3

##Description:
For rebooting modem when your modem is causing your internet speed to slow or not connected.  Code can be modified to use your modem or router.

##Requirments:
* python3, with telnetlib module
* SPEEDTEST CLI program: https://www.speedtest.net/apps/cli
* Telnet enabled on your modem, you can modify code to use modems web interface, I used telnet because it was easyer 

##Install:
Can be run on its own or installed as a systemd service.
To install:
* Enable Remote Management, Remote Console, and set password
* Edit modem-check.py, with password
* Copy script to /usr/local/bin/modem-check.py
    *   sudo cp modem-check.py /usr/local/bin/modem-check.py
* Copy modem-check.service to /etc/systemd/system/modem-check.service
    *   sudo cp modem-check.service /etc/systemd/system/modem-check.service
* Load new service files in systemd
    *   sudo systemctl daemon-reload
* Enable modem-check.service
    *   sudo systemctl enable modem-check


##Systemd Service:
* Enable/Disable
    *   sudo systemctl enable modem-check
    *   sudo systemctl disable modem-check
* Manual start and stop
    * sudo systemctl start modem-check
    * sudo systemctl stop modem-check
* Check status
    *   sudo systemctl status modem-check
* View Logs
    *   sudo journalctl -u modem-check


##Tested:
* Works on CenturyLink Technicolor C2100T
* you may need to change modem_reboot_command or modify the reboot_modem function to get it working for you modem, if you can't use telnet some modems can be restarted via webpage interface 

#Other options:
* https://github.com/cleitonbueno/reboot_router - Reboot D-LINK DWR-922 via web URL
* https://github.com/jvigilan/Reboot_Router -  Reboot router using firefox connectivity
* https://github.com/diveflo/arris-tg3442-reboot - Reboot Arris TG3442* cable modem/router remotely
* https://github.com/sindresorhus/fast-cli - alternative bandwidth test using https://fast.com
* https://github.com/sindresorhus/speed-test - alternative bandwidth test using https://speedtext.net
