download_dependencies.sh: Downloads all dependencies on machine that has Internet access. This was used to easily gather all the dependencies in order for them to be transferred to the isolated VMs.

install_dependencies.sh: Installs all dependencies needed for the server. Run this on the VM on which you want to deploy the server.py on.

clean_server.sh: Deletes session tokens, database, and other files that are created when running the server.

start_server.sh: Runs server.py as a Flask application.

database.py: Creates initial database.

library.py: Contains functions for implementation of database.

server.py: Starts a Flask server for voting. This contains the secured, defended implementation of the server.

tables.sql: SQL source file containing database rules.

unsecured_server.py: Starts a Flask server for voting. This contains the undefended implementation of the server that allows the on-path adversary access to user data.

mitm.py: Script for the on-path adversary. Allows adversary to parse packet payloads to determine user credentials and then make a request to alter their votes.

----- Templates:

webpage.html: Voting user-interface. Contains user login fields, as well as vote selection field. Displays number of votes for each candidate.

loginfail.html: Redirect that is presented to users should they fail to provide suitable login credentials. 

=============================================================

Instructions:

=====Client=====
Note: The client will only work for the un-secured version of the web server as the web page does not involve any javascript, but because the secured version includes javascript browsers such as w3m are not able to run properly. Ensure that a CLI browser such as Brow.SH, lynx, or elinks has been properly installed and configured in order to properly receive requests from the secured server. 

Steps to set up client (if not using built-in cURL to make HTTP requests):
w3m:
sudo apt install w3m w3m-img
To connect to web server at 10.64.13.2 on port 5000 using w3m:
w3m http://10.64.13.2:5000

=====Server=====

Steps to set up web server:
Copy project directory to the VM
scp -P 8247 -r /path/to/project student@secnet-gateway.cs.wpi.edu:~/


SSH into the VM
ssh -p 8247 student@secnet-gateway.cs.wpi.edu


Set up Python virtual environment
Create virtual environment
python3 -m venv app_env

If this fails, run sudo apt-get install python3.8-venv
Activate virtual environment
source app_env/bin/activate

Install Python dependencies
Navigate into project folder that was copied over in step 1
cd project/

Run script to install dependencies
bash install_dependencies.sh

Start web server
Navigate to app folder (located in the project folder)
cd app/

Run script to start server
bash start_server.sh


If the cryptography library is not imported, run steps 4-5 again outside of the python virtual environment. The environment can be exited by typing “deactivate”. This is because the cryptography library is already installed on the Zoo Lab VM’s.

=====On-path Adversary=====

Steps to set up on-path adversary:
Set up all the VM routes

Assuming VM 1 (10.64.13.1) and VM 2 (10.64.13.2) are trying to communicate while VM 3 (10.64.13.3) is the on-path adversary, the following commands should be run:

IP Forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward - Run on VM 3

Static Routes
route add -host 10.64.13.1 gw 10.64.13.3 - Run on VM 2
route add -host 10.64.13.2 gw 10.64.13.3 - Run on VM 1

Stopping ICMP Redirects:
Sending: Put a 0 in: /proc/sys/net/ipv4/conf/*/send_redirects
Receiving:
sysctl net.ipv4.conf.all.accept_redirects=0 net.ipv4.conf.eth0.accept_redirects=0 net.ipv4.conf.eth1.accept_redirects=0

Filtering:
iptables -A INPUT -p icmp --icmp-type redirect -j DROP
iptables -A OUTPUT -p icmp --icmp-type redirect -j DROP

Copy python script to the selected on-path VM
Located under app/mitm.py
Configure the python script by setting these values:
url at the top to the target web server url
iface option in the sniff function to the correct interface (In our case “ens3”)
filter option in the sniff function to the correct port (5000)
Run python script



