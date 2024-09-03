import os
import paramiko
import requests
import json
from datetime import datetime, timezone, timedelta

def ssh_multiple_connections(hosts_info, command):
    users = []
    hostnames = []
    for host_info in hosts_info:
        hostname = host_info['hostname']
        username = host_info['username']
        password = host_info['password']
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=22, username=username, password=password)
            stdin, stdout, stderr = ssh.exec_command(command)
            user = stdout.read().decode().strip()
            users.append(user)
            hostnames.append(hostname)
            ssh.close()
        except Exception as e:
            print(f"用户：{username}，连接 {hostname} 时出错: {str(e)}")
    return users, hostnames

ssh_info_str = os.getenv('SSH_INFO', '[]')
hosts_info = json.loads(ssh_info_str)

command = 'cd ~/domains/alist;pm2 start ./alist -- server'
user_list, hostname_list = ssh_multiple_connections(hosts_info, command)
