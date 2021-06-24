# modem-reboot-bandwith-test

Modem Bandwidth Test and Reboot

Author: ZyMOS
Date: 06/2021
License: GPLv3

Description:
For rebooting modem when your modem is causing your internet speed to slow.

Requirments:
* python3, with telnetlib module
* SPEEDTEST CLI program: https://www.speedtest.net/apps/cli
* Telnet enabled on your modem, you can modify code to use modems web interface, I used telnet because it was easyer 

Tested:
* Works on CenturyLink Technicolor C2100T
* you may need to change modem_reboot_command or modify the reboot_modem function to get it working for you modem, if you can't use telnet some modems can be restarted via webpage interface 

Other options:
* https://github.com/cleitonbueno/reboot_router - Reboot D-LINK DWR-922 via web URL
* https://github.com/jvigilan/Reboot_Router -  Reboot router using firefox connectivity
* https://github.com/diveflo/arris-tg3442-reboot - restart your Arris TG3442* cable modem/router remotely

