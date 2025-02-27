import argparse
import sys
import os

import pexpect



def main():
    if os.geteuid() != 0:
        exit("You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting.")
    parser = argparse.ArgumentParser(prog="Activate VPN",
                                     description="Activate the Georgia Tech VPN")

    parser.add_argument("user")
    parser.add_argument("password")

    parser.add_argument("--server")
    parser.add_argument("--push")
    parser.add_argument("--gateway")
    args = parser.parse_args()

    server = "vpn.gatech.edu" if not args.server else args.server
    user = args.user
    passw = args.password
    push = "push1" if not args.push else args.push
    gateway = "DC" if not args.gateway else args.gateway

    cmd = " ".join(["sudo", "openconnect", server, "-u", user, "--protocol", "gp"])
    proc = pexpect.spawn(cmd)
    print("Starting VPN")
    try:
        proc.expect("Password")
        proc.sendline(passw)

        idx = proc.expect(['Challenge:', "Unexpected"])
        if idx == 1:
            raise Exception("ERROR: Invalid password")
        proc.sendline(push)
        print("Push notification sent")

        idx = proc.expect_exact(["[DC Gateway|NI Gateway]:", "Unexpected"])
        if idx == 1:
            raise Exception("ERROR: Push verification failed")
        proc.sendline(gateway)
        print("VPN should now be active")

    except pexpect.TIMEOUT:
        print("Timeout error occured. Terminating now")
        sys.exit(1)
    except Exception as e:
        print(e)
        print("Error occurred. Terminating now.")
        sys.exit(1)

    text = """
====================================================
Input 'd' to disconnect                            |
Input 'i' to turn on interactive mode              |
Input 'c' to check if the connection is still alive|
Input 'h' to see this list again                   |
===================================================="""

    print(text)
    while True:
        command = input("Input command: ")

        if command.lower() == 'd':
            proc.kill(1)
            print("VPN disconnected")
            break
        elif command.lower() == 'i':
            proc.interact()
            break
        elif command.lower() == 'c':
            if proc.isalive():
                print("Process is still alive")
            else:
                print("Process is appears to be dead")
        elif command.lower() == 'h':
            print(text)
        else:
            print("Command not recognized")
        

if __name__ == '__main__':
    main()
