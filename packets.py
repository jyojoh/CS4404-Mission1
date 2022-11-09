from scapy.all import *

def http_header(packet):
    http_packet = str(packet)
    if http_packet.find("POST / HTTP/1.1"):
        return POST_print(packet)

def GET_print(packet):
    ret =  "********** GET PACKET **********"
    ret += "\n".join(packet.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += "********************************"
    return ret

def POST_print(packet):
    ret =  "********** POST PACKET **********"
    ret += "\n".join(packet.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n"))
    ret += "*********************************"
    return ret

if __name__ == "__main__":
    sniff(iface="lo", prn=http_header, filter="tcp and port 5000")
