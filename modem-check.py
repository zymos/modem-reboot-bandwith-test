#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################################################################################################################################
#   Modem Bandwidth Test and Reboot
#
#   Author: ZyMOS
#   Date: 06/2021
#   License: GPLv3
#
#   Description:
#       For rebooting modem when your modem is causing your internet speed to slow.
#
#   Requirments:
#       python3, with telnetlib module
#       SPEEDTEST CLI program: https://www.speedtest.net/apps/cli
#       Telnet enabled on your modem, you can modify code to use modems web interface, I used telnet because it was easyer 
#
#   Tested:
#       Works on CenturyLink Technicolor C2100T
#       you may need to change modem_reboot_command or modify the reboot_modem function to get it working for you modem,
#       if you can't use telnet some modems can be restarted via webpage interface 
#
#   Other options:
#       https://github.com/cleitonbueno/reboot_router - Reboot D-LINK DWR-922 via web URL
#       https://github.com/jvigilan/Reboot_Router -  Reboot router using firefox connectivity
#       https://github.com/diveflo/arris-tg3442-reboot - restart your Arris TG3442* cable modem/router remotely
#
######################################################################################################################################





######################################################################################################################################
# Configure
#
bandwidth_limit = 5 # Mbps (remember you may be downloading stuff when test is preformed, so keep it low)
sleep_time = 30 * 60 # sleep time between bandwidth tests (seconds)
sleep_time_fail = 2 * 60 # sleep time between bandwidth tests when bandwidth is less than bandwidth_limit (seconds)
sleep_time_retry = 10 # sleep time if speed_test_command fails for some reason (seconds)
sleep_time_reboot = 90 # sleep time it takes for modem to reboot, should be greater than actual time for modem to reconnect to internet (seconds)
low_speed_test_retrys = 5 # number of failed bandwidth tests before rebooting modem

modem_ip = '192.168.0.1'
modem_username = 'adminlogin' # modems telnet user name
modem_pass = 'Tel0the0net0to0work' # modems telnet password
modem_reboot_command = 'reboot' # modems telnet command for rebooting

speed_test_command=['/usr/local/bin/speedtest-cli', '--csv', '--no-upload'] # command for bandwith test, must be in a list

test_url = 'https://google.com' # to test internet connectivity



######################################################################################################################################
# Code
#
import re
import os
import subprocess
from time import sleep
import telnetlib
import urllib.request
import datetime


# dont actually reboot
test = False # using in debuging
if test:
    bandwidth_limit = 100 # Mbps
    sleep_time = 60 #  
    sleep_time_fail = 5  
    sleep_time_retry = 1 
    sleep_time_reboot = 6 



def parse_args():
    """
    CLI Arguments
    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--reboot', help="Just reboot the modem and exit", action="store_true")
    parser.add_argument('--no-reboot', help="Run speed tests, but no reboot", action="store_true")
    parser.add_argument('--debug', help="prints debug info", action="store_true")

    args = parser.parse_args()
    
    return args


def test_connection(host=test_url):
    '''
    Check if modem is connected to internet
    '''
    try:
        urllib.request.urlopen(host) #Python 3.x
        #  print("Internet connection: OK")
        return True
    except:
        print(str(datetime.datetime.now()) + "> Internet connection: Failed, retrying in " + str(sleep_time_fail) + "s")
        return False
# End: test_connection()




def test_speed(low_speed_count):
    '''
    Tests internet speed
    '''    
    
    # reset sleep time
    sleeping = sleep_time

    # run speed test command
    output = subprocess.run(speed_test_command, capture_output=True, text=True)
    
    # command failed
    if output.stderr:
        sleeping = sleep_time_retry
        print(str(datetime.datetime.now()) + "> Test command failed for some reason, retry in, " + str(sleeping) + 's')
    else:
        #command succeded

        download_speed = re.sub(r"^[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,[^,]*,", '', str(output.stdout))
        download_speed = round(float(re.sub(r",.*", "", download_speed))/1000000) # Mbps

        # Check low speed
        if(download_speed < bandwidth_limit):
            # speed is below limit
            sleeping = sleep_time_fail
            print(str(datetime.datetime.now()) + '> Bandwidth is low: ' + str(download_speed) + "Mbps, failed " + str(low_speed_count) + ' times, retry in ' + str(sleeping) + 's',  flush=True)
            low_speed_count += 1
            #  modem_output = subprocess.run(modem_reboot_command, capture_output=True, text=True)
        else:
            # speed is ok
            print(str(datetime.datetime.now()) + '> Bandwidth OK: ' + str(download_speed) + 'Mbps, next test in ' + str(sleeping) + 's', flush=True)
            sleeping = sleep_time
            low_speed_count = 1

    # too many low speed tests, reboot time
    if low_speed_count > low_speed_test_retrys:
        print(str(datetime.datetime.now()) + '> Bandwidth problem, Rebooting Modem.', flush=True)
        low_speed_count = 1
        sleeping = sleep_time_reboot
        # reboot the modem
        reboot_modem()

    return low_speed_count, sleeping
# End: test_speed()





def reboot_modem():
    '''
    reboot modem via telet
    '''
    

    print('Opening telnet to reboot modem.')
    try:
        with telnetlib.Telnet(modem_ip, timeout=10) as tn:
            tn.set_debuglevel(0)    # debug info is useful
            tn.read_until(b'Login:', 10)               # waits until it recieves a string 'login:'
            tn.write(modem_username.encode('ascii'))         # sends username to the server
            tn.write(b'\r')                            # sends return character to the server
            tn.read_until(b'Password:', 10)            # waits until it recieves a string 'Password:'
            tn.write(modem_pass.encode('ascii'))         # sends password to the server
            tn.write(b'\r')   
            sleep(2)
            tn.read_until(b'>', 10)            # waits until it recieves a string 'Password:'
            if test:
                # run a basic command to test
                print(str(datetime.datetime.now()) + "> Running benine telnet command")
                tn.write(('meminfo').encode('ascii'))             # sends a command to the server
                tn.write(b'\r')
                tn.write(b"exit\r")
                print(tn.read_all())
            else:
                tn.write(modem_reboot_command.encode('ascii'))             # sends a command to the server
                tn.write(b'\r')
                sleep(2)    # need to sleep before closing telnet, otherwise modem won't reboot
            # close the instance
            tn.close()

    # telnet failed, check the modem
    except EOFError:
        print(str(datetime.datetime.now()) + "> Telnet: Unexpected response from modem")
        exit()
    except ConnectionRefusedError:
        print(str(datetime.datetime.now()) + "> Telnet: connection refused by modem. Telnet enabled?")
        exit()
    except:
        print(str(datetime.datetime.now()) + "> Telnet: Error")
        exit()

    # wait for modem to restart
    print(str(datetime.datetime.now()) + "> Waiting for modem to restart")
    return()
# End: reboot_modem



def main():
    '''
    Main function
    '''
    args = parse_args()

    if args.reboot:
        # reboot modem only
        print("Rebooting modem.")
        reboot_modem()
        exit()

    low_speed_count = 1

    print("Testing modem connection bandwidth, will reboot modem if bandwidth < " + str(bandwidth_limit) + 'Mbps', flush=True)
    #  exit()
    while True:
        # reset sleep time
        sleeping = sleep_time

        # Internet Connection Test: if connection is up
        if not test_connection():
            # internet connection Failed
            low_speed_count += 1
            sleeping = sleep_time_fail 
        else:
            # Intenet connection OK
            # run speed test command
            low_speed_count, sleeping = test_speed(low_speed_count)


         # too many low speed tests, reboot time
        if low_speed_count > low_speed_test_retrys:
            print(str(datetime.datetime.now()) + '> Bandwidth problem, Rebooting Modem.', flush=True)
            low_speed_count = 1
            sleeping = sleep_time_reboot
            # reboot the modem
            reboot_modem()

        # Sleep with varable time depending on 
        sleep(sleeping)

# initalize
if __name__ == "__main__":
    main()
