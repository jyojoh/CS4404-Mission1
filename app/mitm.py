from scapy.all import *

load_layer("http")

def http_header(packet):
        http_packet=str(packet)
        if http_packet.find('POST'):
                print(GET_print(packet))
        print(packet)
def GET_print(packet1):
        print("***************************************GET PACKET****************************************************")
        print("\n".join(packet1.sprintf("{Raw:%Raw.load%}\n").split(r"\r\n")))

        print("*****************************************************************************************************")


sniff(iface="Intel(R) I211 Gigabit Network Connection", prn = http_header, filter = "port 80")