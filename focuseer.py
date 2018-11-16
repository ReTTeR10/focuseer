import sys
import subprocess
import re
import time
 

def operate(command):
    args = ['printf']
    args.append(command)
    args2 = ['./lmox', '-r 115', '-D /dev/ttyUSB0']
    process_curl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,stdout=subprocess.PIPE, shell=False)
    process_curl.stdout.close()
    result = process_wc.communicate()[0]
    return result.decode()

def main():
    device = "/dev/ttyUSB0"
    baud = "115"
    homed = False
    stoped = False
    home_cmd = "10 81"
    print('''
    Allowed commands: \n 
    1) init - initialize controller
    2) home - move focuseer to limit switch
    3) move - move focuseer (need stop)
    4) stop - stop moving
    5) exit or quit - exit programm
    ''')


    while(True):
        input_str = input(">> ")
        if input_str == "init":
            cmd = '10 87'
            result = operate(cmd)
            if "ACY" in str(result) or "DCS" in str(result): 
                print("init ready")

        elif input_str == "home":
            cmd = "10 e1"
            result = operate(cmd)
            while "DCS" in result:
                result = operate(cmd)
                time.sleep(0.1)
            
            if "02" not in result:
                homed = False
                cmd = "10 82"
                result = ""
                result = operate(cmd)

                cmd = "10 e1"

                while "02" not in str(result):       # <Data 1 bytes: 02         00 - NOT HOME
                    result = operate(cmd)
                    #print(result)
                    print('.', end='', flush=True)
                    time.sleep(0.5)
                print()
                

            print("Home ready")
            homed = True
        
        
        elif input_str == "stop":
            args = '10 80'
            result = operate(args)
            if "ACY" in str(result) or "DCS" in str(result): 
                print("stop ready")
                stoped = True

        # elif input_str == "move":
        #     args = ['printf', '10 81']
        #     result = operate(args)
        #     print(result)
        #     print("move accept")
        #     if "ACY" in str(result) or "DCS" in str(result): 
        #         print("moving...")
        #         args = ['printf', '10 a0']
        #         while True:
        #             result = operate(args)
        #             pos = 0
        #             print(result)
        #             try:
        #                 pos = int("".join(result.replace("<Data 3 bytes: ", "").split(" ")[::-1]), 16)
        #                 print("Position = {}".format(pos))
        #             except:
        #                 pass
        #             if pos >= 60000:
        #                 print("ready")
        #                 break
                
        elif input_str == "exit" or input_str == "quit":
            break
        
        elif not input_str:
            pass

        else:
            print("\"{}\" is invalid command".format(input_str))
if __name__ == "__main__":
    main()