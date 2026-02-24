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
Ans: We used the command "sudo systemctl status ssh" to verify that SSH is active. The output snippet shows that the SSH service is active.

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

**RQ11: Is system time correct? If not, what could break downstream (give two examples)?**  
Ans: System time is correct, incorrect system time triggers "silent" downstream failures:
1. SSL/TLS Failures: Security certificates have strict validity periods. Outdated system time causes tools like apt and pip to reject connections as "insecure," blocking updates and installations.
2. Build & Cache Issues: Tools like Python’s internal caching rely on timestamps.

**RQ12: How much free disk space is available? Why does disk usage matter for logging systems**  
Ans: The available disk space is ~35.7GBytes. The disk usage for logging systems matters because if the disk space runs out, critical system operations may halt, which can prevent the administrators from diagnosing bugs and issues.

**RQ13: What Python version is installed? Why might the Python version affect reproducibility?**  
Ans: Python 3.13 with pip 25.1.1. Based on the python version certain programs may not run, or compile correctly, so we need to make sure we work on the same version of python both on our personal computer and raspberry pi.

**RQ14: Who created the repository and how did you grant access to teammates (briefly)?**  
Ans: One member of the team created the repository. Then he added the rest of the team members as collaborators.

**RQ15:  What would likely go wrong if each team member kept their own local version of the lab/project work?**  
Ans: If each team member kept their own local version of the lab/project work, the project faces three critical risks: code divergence & merge conflicts, loss of accountability & Rollbacks, manual syncing errors 

**RQ16: What is the difference between git add and git commit (in your own words)?**  
Ans: git add: Selects and moves specific file changes to the Staging Area (the "loading dock") to prepare them for the next update.
git commit: Creates a permanent, timestamped snapshot of all staged changes in the project history with a descriptive message.

**RQ17: What does git push do, and why is it important in a team setting?**  
Ans: The git push command pushes all the changes that were created by a singular user to the github repository so that the rest of the team's members have access to the new source code.

**RQ18: Can you think what problem can happen if two teammates edit the same file without pulling first?**  
Ans: If 2 people edit the same file without pulling first, there will be conflicts. Conflicts happen when the user removes, or adds new lines of code that overlap the change of the other user. 

**RQ19: Did your team use branches? If yes, describe your workflow briefly. If no, explain why.**  
Ans: We used branch for test purposes. Specifically, we created a test branch, named `my-test-branch`. The change made in the repository is the creation of a test file name `test.txt`, location: `labs/lab01/test.txt`

**RQ20: What is a merge conflict, and when does it happen?**    
Ans: A merge conflict is when changes have been made to the same part of a file by two people or more when we push the file in a github repository.

**RQ21: Which authentication method did you use to push to GitHub (HTTPS+token, SSH key, other)? Why?**  
Ans: On our personal computer, each team member uses the SSH key from their laptop. On the raspberry pi we have setup an SSH key that we linked with our repository, since HTTPS password authentication is not supported for Git operations. That way we can have access to a private repository, and push/pull access. 

**RQ22: Why should virtual environments not be committed to git?**  
Ans: Virtual environments are machine-specific and do not work on different computers and take up a lot of space unnecessarily.

**RQ23: Why is it usually not acceptable to commit logs?**  
Ans: Logs do not contain a part of the source code, and are large files that can slow down operations.

**RQ24: Where on the Pi did you clone the repo (path)? Why did you choose that location?**  
Ans: The home directory of the raspberry Pi, that is also the first directory of the terminal. This way we can access faster the lab's files instead of navigating through the `change directory (cd)` command.

**RQ25: What did sys.executable show, and how does that prove you are using the venv?**  
Ans: `sys.executable` output: `/home/iotlab_upat_5/venv/bin/python`
Significance: This confirms the shell is using the isolated Python interpreter located within the project's local venv directory, rather than the global system-wide Python. 

**RQ26: In one paragraph: what problem does a venv solve?**  
Ans: A venv solves the problem of dependency conflicts between different python projects by creating isolated environments where each project can have its own set of installed packages and specific versions, without interfering with the global Python installation or other projects.

**RQ27: What dependencies did you include and why? If you use argaprse do you need to include the requirements.txt, if not why?**  
Ans: Since we are testing the venv we download the click module for a better structured CLI. We add the click version in the requirements.txt file (click==8.1.7). The argaprse package comes installed with any python version >=3.2, so we do not need to include it in the requirents.txt file.

**RQ28: What would happen if different teams used different dependency versions?**  
Ans: Using different dependency versions across teams leads to "broken" code where specific features or libraries might be missing or incompatible, causing the program to fail. That's why we use virtual environments, in order to isolate each project's dependencies, ensuring that every team member runs the exact same environment and preventing conflicts with system-wide packages.

**RQ29: How can you verify you installed packages into the venv (not the system Python)? Give one command and explain what you look for.**  
Ans: Run pip list after activating your virtual environment. If the packages you installed appear in the output, they are installed in the venv. 
