# rexec
send remote command through paramiko via ssh.

> attention: we assume that your command will surely be finished in limited time, and this program will output nothing before your command is done on the remote server.

## install

1. go [https://github.com/GGN-2015/rexec/releases](https://github.com/GGN-2015/rexec/releases) and download a `.whl` file.
2. use `pip install rexec-<version>-py3-none-any.whl` to install the package into your local environment.

## usage

### send remote command to server  via ssh

you need to fill in six parameters in the following order, if you are not sure about the `<port>` argument, try to let `<port>` equal to `22`.

```bash
python3 -m rexec <user> <host> <cmd> <password> <port>
```

### wihtout password

if you have configured an auto login with `~/.ssh/authorized_keys`, you can just leave `<password>` blank as follows:

```bash
python3 -m rexec <user> <host> <cmd> "" <port>
```

### sample

here is a sample usage of this package, this will output a detailed list of file under the home folder of the user named "admin".

```bash
python3 -m rexec "admin" "192.168.0.1" "cd ~; ls -alh" "1145141919810" 22
```

