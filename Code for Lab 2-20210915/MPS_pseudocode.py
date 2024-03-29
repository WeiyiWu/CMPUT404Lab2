#!/usr/bin/env python3
import socket, time, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024

#TO-DO: get_remote_ip() method
def get_remote_ip():
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print('Hostname could not be ')
        sys.exit()

    print(f'Ip address of {host} is {remote_ip}')
    return remote_ip

#TO-DO: handle_request() method
def handle_request():
    #connect proxy_end
    proxy_end.connect((remote_ip, port))

    #send data
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending recieved data {send_full_data} to google")
    proxy_end.sendall(send_full_data)

    #remember to shut down
    proxy_end.shutdown(socket.SHUT_WR) #shutdown() is different from close()

    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending recieved data {data} to client")
    #send data back
    conn.send(data)

def main():
#TO-DO: establish localhost, extern_host (google), port, buffer size
    extern_host = 'www.google.com'   
    port = 80
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: #establish "start" of proxy (connects to localhost)
#       TO-DO: bind, and set to listening mode
        print("Starting proxy server")
        #allow reused addresses, bind, and set to listening mode
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(2)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: #establish "end" of proxy (connects to google)
            #TO-DO: get remote IP of google, connect proxy_end to it
            print("Connecting to Google")
            remote_ip = get_remote_ip(extern_host)

            #now for the multiprocessing...

            #TO-DO: allow for multiple connection with a Process daemon
            # make sure to set target = handle_request when creating the Process
            while True:
            #accept connections and start a Process daemon for handling multiple connection
                conn, addr = s.accept()
                p = Process(target=handle_request(), args=(addr, conn))
                p.daemon = True
                p.start()
                print("Started process ", p)

        #TO-DO: close the connection!
                conn.close()

if __name__ == "__main__":
    main()