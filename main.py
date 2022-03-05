import socket
from requests import get
from hashlib import sha1
import time

username="loaderH"


#server=get("https://server.duinocoin.com/getPool")
#if server.status_code!=200:
#    print("Error get socket ip and port!")
#    exit(1)

#response=server.json()
response={"ip":"162.55.103.174","name":"diskos-pool-1","port":6000,"server":"duino-svko-1","success":True}
ip=response['ip']
port=response['port']
sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip,port))
version=sock.recv(100).decode()
print(f"Server version: {version}")

while True:
    sock.send(f"JOB,{username},LOW".encode())
    job=sock.recv(1024).decode().strip().split(",")

    base_hash=sha1(job[0].encode())
    start_time = time.time()
    for i in range(int(job[2])*100+1):
        tmp=base_hash.copy()
        tmp.update(str(i).encode())
        ducos=tmp.hexdigest()
        if job[1]==ducos:
            timeDifference = time.time() - start_time
            hashrate = i / timeDifference
            sock.send(f"{i},{hashrate},Python_MY_PC_Miner,MyMiner".encode())
            feedback=sock.recv(1024).decode().strip()
            if feedback=="GOOD":
                print(f"Successful hash result:{i} hashrate:{int(hashrate/1000)}Kh/s Difficulty:{job[2]}\r",end="")
            else:
                print(f"Error hash!")
            break
    #print(job)
