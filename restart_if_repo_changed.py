import subprocess
import os

def run_bash_command(command):
    ## call date command ##
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    
    ## Talk with date command i.e. read data from stdout and stderr. Store this info in tuple ##
    ## Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached.  ##
    ## Wait for process to terminate. The optional input argument should be a string to be sent to the child process, ##
    ## or None, if no data should be sent to the child.
    (output, err) = p.communicate()
    
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    print ("Command output : ", output)
    print ("Command exit status/return code : ", p_status)
    return output



up_to_date = run_bash_command("cd /data/test && [ $(git rev-parse HEAD) = $(git ls-remote $(git rev-parse --abbrev-ref @\{u\} | \
sed 's/\// /g') | cut -f1) ] && echo -n 400 || echo -n 200")

print(int(up_to_date))

if int(up_to_date)==200:
            print('I am here')
            run_bash_command('sudo kill $(pgrep -f \'python3 /data/test/httpsrv.py\')')
            run_bash_command('cd /data/test && sudo git pull origin master')
            run_bash_command('sudo python3 /data/test/httpsrv.py > /dev/null 2>&1 &')
            
                        



