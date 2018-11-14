import sys
import subprocess

def operate(command):
    args = command
    args2 = ['./lmox', '-r 115', '-D /dev/ttyUSB0']
    process_curl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,stdout=subprocess.PIPE, shell=False)
    # Allow process_curl to receive a SIGPIPE if process_wc exits.
    process_curl.stdout.close()
    result = process_wc.communicate()[0]
    print(result)
    return result

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
            args = ['printf', '10 87']
            # args2 = ['./lmox', '-r 115', '-D /dev/ttyUSB0']

            # process_curl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
            # process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,stdout=subprocess.PIPE, shell=False)
            # # Allow process_curl to receive a SIGPIPE if process_wc exits.
            # process_curl.stdout.close()
            # result = process_wc.communicate()[0]
            # print(result)
            result = operate(args)
            if "ACY" in str(result) or "DCS" in str(result): 
                print("init ready")

        elif input_str == "home":
            args = ['printf', '10 82']
            # args2 = ['./lmox', '-r 115', '-D /dev/ttyUSB0']

            # process_curl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
            # process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,stdout=subprocess.PIPE, shell=False)
            # # Allow process_curl to receive a SIGPIPE if process_wc exits.
            # process_curl.stdout.close()
            # result = process_wc.communicate()[0]
            # print(result)
            result = operate(args)
            if "ACY" in str(result) or "DCS" in str(result): 
                print("home ready")
                homed = True
        
        elif input_str == "stop":
            args = ['printf', '10 80']
            # args2 = ['./lmox', '-r 115', '-D /dev/ttyUSB0']

            # process_curl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
            # process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,stdout=subprocess.PIPE, shell=False)
            # # Allow process_curl to receive a SIGPIPE if process_wc exits.
            # process_curl.stdout.close()
            # result = process_wc.communicate()[0]
            # print(result)
            result = operate(args)
            if "ACY" in str(result) or "DCS" in str(result): 
                print("stop ready")
                stoped = True

        elif input_str == "move":
            args = ['printf', '10 81']
            # args2 = ['./lmox', '-r 115', '-D /dev/ttyUSB0']

            # process_curl = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
            # process_wc = subprocess.Popen(args2, stdin=process_curl.stdout,stdout=subprocess.PIPE, shell=False)
            # # Allow process_curl to receive a SIGPIPE if process_wc exits.
            # process_curl.stdout.close()
            # result = process_wc.communicate()[0]
            # print(result)
            result = operate(args)
            if "ACY" in str(result) or "DCS" in str(result): 
                print("moving")
                
            
            
                
        elif input_str == "exit" or input_str == "quit":
            break

if __name__ == "__main__":
    main()