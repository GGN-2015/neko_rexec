import paramiko
import random
import string



# generate random string
def generate_random_string(length) -> str:
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string



# get output within the range of user command
def get_useful_content(raw_content: bytes, cmd: bytes, begin_tag: bytes, end_tag: bytes) -> bytes:
    cutted = raw_content.split(begin_tag)[-1].split(end_tag)[0].rstrip()
    if len(cmd) > 0 and cutted.startswith(cmd):
        cutted = cutted[len(cmd):] # erase the echo of the input command
    if cutted.endswith(b"echo"):
        cutted = cutted[:-len("echo")] # erase echo at the end of stdout
    return cutted.rsplit(b"\x1b", maxsplit=1)[0].split(b"\r\n", maxsplit=1)[-1]



# send a remote command to some server via ssh
# if ssh auto login has been configured, just leave password=""
def send_remote_cmd(username: str,hostname: str, command: str, password: str, port=22):

    # use random guard
    BEGIN_TAG = generate_random_string(128).encode()
    END_TAG   = generate_random_string(128).encode()

    # establish a ssh connection
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=port, username=username, password=password)
    transport = ssh.get_transport()
    channel   = transport.open_session()
    channel.get_pty("vt100", width=80, height=24)
    channel.invoke_shell()
    stdin  = channel.makefile("wb", -1)
    stdout = channel.makefile("rb", -1)
    stderr = channel.makefile_stderr("rb", -1)

    # use stdin to communicate with the terminal
    command = command.strip().encode("utf-8")
    stdin.write(b"PS1=\"\"\n")
    stdin.write(b"echo %s ; %s\n" % (BEGIN_TAG, command))
    stdin.write(b"echo %s ;   \n" % (END_TAG))
    stdin.write(b"exit\n")
    stdin.close()
    stdout_content = stdout.read() # this function will not return until stdin is closed
    stderr_content = stderr.read()
    ssh.close()

    # get the output in command range
    stdout_content = get_useful_content(stdout_content.strip(), command, BEGIN_TAG, END_TAG)
    return stdout_content, stderr_content