# IP Substitute
Simple tool to substitute some parts of a string with IP and port. Requires `netifaces` package.

# Usage
```
python3 ipsub.py [-h] [-i IFACE] [-p PORT] [-ips IPSUB] [-ps PTSUB] [-subs]
                 [-ns] [-v]
                 input [input ...]
```

# Example
Simple substitution ("IP" will be replaced with ip, "PT" will be replaced with port):
```
$ python3 ipsub.py wget http://IP:PT/foo/bar
wget http://192.168.1.3:9999/foo/bar
```
Change network interface:
```
$ python3 ipsub.py wget http://IP:PT/foo/bar -i tun0
wget http://192.168.50.5:9999/foo/bar
```
Change IP and port substitution string:
```
$ python3 ipsub.py wget http://IPADDR:PORT/foo/bar -ips IPADDR -ps PORT
wget http://192.168.1.3:9999/foo/bar
```
Change port number:
```
$ python3 ipsub.py wget http://IP:PT/foo/bar -p 80
wget http://192.168.1.3:80/foo/bar
```
Remove space from output:
```
$ python3 ipsub.py wget http://IP:PT/foo/bar -ns
wgethttp://192.168.1.3:9999/foo/bar
```
Substitute space with `${IFS}`:
```
$ python3 ipsub.py wget http://IP:PT/foo/bar -subs
wget${IFS}http://192.168.1.3:9999/foo/bar
```
Commands with other custom flags:
```
$ python3 ipsub.py "wget http://IP:PT/foo/bar -O out -q" -i tun0
wget http://192.168.50.5:9999/foo/bar -O out -q
```

# Setup
```
$ pip3 install -r requirements.txt
```

