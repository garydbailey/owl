import socket
import struct
import sys
import untangle

multicast_group = '224.192.32.19'
server_address = ('', 22600)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind to the server address
sock.bind(server_address)

# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# function to extract the current property consumption
def proppower(owlmessage):
    strmessage = untangle.parse(owlmessage.decode("utf-8"))
    try:
        current_power = strmessage.electricity.property.current.watts.cdata
        return(current_power)
    except:
        return("-1")


# Receive/respond loop
while True:
    #print >>sys.stderr, '\nwaiting to receive message'
    print('Waiting to receive message')
    data, address = sock.recvfrom(1024)
    
    #print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    #print >>sys.stderr, data
    print('Received ',str(len(data)), ' bytes')

    #print >>sys.stderr, 'sending acknowledgement to', address
    #sock.sendto('ack', address)
    print(str(data))
    power = proppower(data)
    if (power) != "-1":
        print("Current Power Consumption = ", power)


