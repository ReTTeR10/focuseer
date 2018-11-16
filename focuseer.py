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

def mm_to_pos(mm_value):
    return int(3875.968992248062 * mm_value) 

def pos_to_mm(pos):
    return 0.000258 * pos

def byte_to_pos(byte_string):
    pos = int("".join(byte_string.split(" ")[::-1]), 16)
    return pos

def pos_to_byte(position):
    byte_string = "00 00 00"
    if position >= 0:
        unshifted_hex = "{:06x}".format(position)
        byte_string = unshifted_hex[4:6] + " " + unshifted_hex[2:4] + " " + unshifted_hex[0:2]
    else:
        unshifted_hex = "{:06x}".format(int("0xffffff", base=16) + 1 + position)[-6:]
        byte_string = unshifted_hex[4:6] + " " + unshifted_hex[2:4] + " " + unshifted_hex[0:2]

    return byte_string

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
    4) getpos - get current position
    5) stop - stop moving
    6) exit or quit - exit programm
    ''')


    while(True):
        input_str = input(">> ")

        p = re.compile(r"move ([0-9]*[.])?[0-9]+")
        match = p.match(input_str)

        if input_str == "init":
            cmd = '10 87'
            result = operate(cmd)
            cmd = '10 34 40 10'
            result = operate(cmd)
            cmd = '10 36 70 00'
            result = operate(cmd)

            if "ACY" in str(result) or "DCS" in str(result): 
                print("init ready")

        elif input_str == "home":
            cmd = "10 e1"                # check teminal swich
            result = operate(cmd)
            while "DCS" in result:
                result = operate(cmd)
                time.sleep(0.1)
            
            if "02" not in result:
                homed = False
                cmd = "10 82"            # move until terminal swich reached
                result = ""
                result = operate(cmd)

                cmd = "10 e1"            # check terminal swich 

                while "02" not in str(result):       # <Data 1 bytes: 02   00 - NOT HOME
                    result = operate(cmd)
                    #print(result)
                    print('.', end='', flush=True)
                    time.sleep(0.5)
                print()
            
            cmd = "10 88"               # Reset asbolute position counter
            result = operate(cmd)
            while "ACY" not in result:
                result = operate(cmd)
                time.sleep(0.1)

            print("Home ready")
            homed = True
        
        elif input_str == "stop":
            args = '10 80'
            result = operate(args)

            args = '10 86'
            result = operate(args)

            if "ACY" in str(result) or "DCS" in str(result): 
                print("stop ready")
                stoped = True
        
        elif match:
            target_position = mm_to_pos(float(match[0].replace("move ", "")))
            # print(target_position)
            cmd = "10 a0"                # Read current absolut position
            result = operate(cmd)
            while "DSC" in result and "Data 3 bytes" not in result:
                result = operate(cmd)
                time.sleep(0.1)

            current_position = byte_to_pos(result[51:-3])
            cmd  = "10 03 " + pos_to_byte(target_position - current_position) #set target position
            #printtarget_position - current_position)
            #print(cmd)
            result = operate(cmd)
            cmd = "10 84"                  # Move to target position    
            result = operate(cmd)
            
        elif input_str == "getpos":
            cmd = "10 a0"                # Read current absolut position
            result = operate(cmd)
            while "DSC" in result and "Data 3 bytes" not in result:
                result = operate(cmd)
                time.sleep(0.1)

            current_position = byte_to_pos(result[51:-3])
            #print(pos_to_mm(current_position))


        elif input_str == "exit" or input_str == "quit":
            break
        
        elif not input_str:
            pass

        else:
            print("\"{}\" is invalid command".format(input_str))
if __name__ == "__main__":
    main()