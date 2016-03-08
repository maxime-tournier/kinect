import kinect
import json

def make_table():
    table = {}
    for j in kinect.JointType._values_.values():
    
        part = j.lower().split('joint')[-1].split('_')[1:]

        name = part[-1]

        if len(part) is 2:
            name = part[0][0] + name

        table[j] = name

    return table

table = make_table()

def source():
    for users in kinect.tracked():
        frame = {}

        for i, u in users.iteritems():
            frame[ i ] = {}

            for t, j in kinect.joints(u):
                name = table[kinect.JointType._values_[t.value]]
                data = [j.x, j.y, j.z]
                frame[ i ][name] = data

        yield json.dumps(frame)



import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 6969
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

while True:
    print 'waiting for client...'
    conn, addr = s.accept()
    print 'connection from:', addr

    try:
        for data in source():
            conn.send( data + '\n' )
            
    except socket.error, msg:
        print 'client error:', msg
    finally:
        conn.close()
