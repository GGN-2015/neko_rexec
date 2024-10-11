import sys
from .send_remote_cmd import send_remote_cmd



# check argv number
# attention: 
#   it is not wise to use password in command line.
#   you can just leave password="" if you have configured an auto login with something like `~/.ssh/authorized_keys`
if len(sys.argv) != 6:
    sys.stderr.write("usage: python3 -m rexec <user> <host> <cmd> <password> <port>\n")
    sys.stderr.write("       use "" as <password> if you have configured auto login.\n")
    exit(1)



# load data from argv
argv_user = sys.argv[1]
argv_host = sys.argv[2]
argv_cmmd = sys.argv[3]
argv_pswd = sys.argv[4]
try:
    argv_port = int(sys.argv[5])
except:
    argv_port = 22 # use default port when error ocurs



# exec a command on remote server
# the command will be executed as is inputed to a terminal
stdout_content, stderr_content = send_remote_cmd(argv_user, argv_host, argv_cmmd, argv_pswd, argv_port)
sys.stdout.write(stdout_content.decode("utf-8") + "\n")
sys.stderr.write(stderr_content.decode("utf-8"))