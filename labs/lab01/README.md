## Section B: Report

**RQ1: What hostname and IP address did you use?**
Ans: Hostname: iotlab-Upat-5
IP Address: 192.168.137.244

**RQ2: Did DNS resolution work (ping google.com)? If it failed, what does that imply?**
Ans: Yes, DNS resolution worked succesfully. It implies that the Raspberry Pi has access to a DNS server and can resolve domain names to IP addresses. If it had failed while ping 8.8.8.8 worked, it would mean the device had internet access but couldn't reach a DNS server to translate names.

**RQ3: Was the connection wired or wireless?**
Ans: The connection was wireless.
Evidence: The ip a output shows the eth0 (wired) interface as DOWN and NO-CARRIER, while the wlan0 (wireless) interface is UP with an assigned IP address of 192.168.137.244.

**RQ4: Which method did you use to enable SSH (GUI or raspi-config)? List the exact steps.**
Ans: We used the command line configuration method. Steps:
1. Open the terminal
2. Type "sudo raspi-config"
3. Select "Interface Options"
4. Select "SSH"
5. Choose "Enable"
6. Reboot manually once.

**RQ5: What command did you run to verify that SSH is active? Include the relevant output snippet.**
Ans: We used the command "sudo systemctl status ssh" to verify that SSH is active. The output snippet shows that the SSH service is active (running).
![alt](image.png) 

**RQ6: In your own words, why is SSH a necessary tool for managing edge devices after deployment?**
Ans: It's necessary for remote management of edge devices after deployment. It allows for secure, headless connections with authentication and more automated setup.

**RQ6: What SSH command did you use, and which username ?**
Ans: `ssh iotlab-upat-5@192.168.137.244`
username: iotlab-upat-5

**RQ7: Did you see a host key prompt the first time? What is that prompt for (in your own words)?**
Ans: Yes, we saw the host key prompt the first time. It is the first authentication, without SSH key, that asks us to confirm the host key and enter the password we set.

**RQ8: What does uptime tell you that is relevant for edge systems?**
Ans: The uptime command provides key health metrics for edge systems:

1. System Time: Ensures accurate logs and data synchronization.
2. Uptime Duration: Tracks stability and helps detect unexpected reboots.
3. Active Users: Monitors current SSH sessions and remote access.
4. Load Average: Shows CPU workload to ensure the edge device isn't overwhelmed. 

**RQ9: Did you enable SSH keys? describe the steps briefly.**
Ans: Yes, we enabled SSH key-based authentication using the following steps in Git Bash:

1. Generated a new SSH key pair using `ssh-keygen -t ed25519`.
2. Verified the creation of the public and private keys with `ls ~/.ssh`.
3. Started the SSH agent using `eval "$(ssh-agent -s)"` and added the private key with `ssh-add ~/.ssh/id_ed25519`.
4. Copied the public key to the Raspberry Pi using `ssh-copy-id iotlab_upat_5@192.168.137.244` to allow passwordless login.

**RQ10: Why are SSH keys generally preferred over passwords for remote access?**
Ans: SSH keys are preferred for two main reasons:
1. Security: They are much more resistant to brute-force attacks than passwords.
2. Convenience: They enable faster, passwordless, and automated remote access.