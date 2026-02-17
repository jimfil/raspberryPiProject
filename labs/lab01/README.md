## Section B: Report

**RQ1: What hostname and IP address did you use?**
Ans: Hostname: iotlab-Upat-5
IP Address: 192.168.137.244

**RQ2: Did DNS resolution work (ping google.com)? If it failed, what does that imply?**
Ans: Yes, DNS resolution worked succesfully. It implies that the Raspberry Pi has access to a DNS server and can resolve domain names to IP addresses. If it had failed while ping 8.8.8.8 worked, it would mean the device had internet access but couldn't reach a DNS server to translate names.

**RQ3: Was the connection wired or wireless?**
Ans: The connection was wireless.
Evidence: The ip a output shows the eth0 (wired) interface as DOWN and NO-CARRIER, while the wlan0 (wireless) interface is UP with an assigned IP address of 192.168.137.244.

