FTP Analyzer - Passive FTP Traffic Sniffer

`ftp_analyzer` is a lightweight, CLI-based tool built in Python to monitor and analyze FTP traffic on a given network interface.

It is designed for ethical hacking, traffic analysis, and detection of insecure FTP usage. This tool passively listens for FTP connections, logs activity, and detects clear-text credentials (usernames & passwords). It also monitors connection frequency and flags IPs showing suspicious behavior — such as brute-force attempts or mass scanning.

Features

- 📡 **Passive FTP Sniffing** – No active interference or MITM; listens quietly on TCP port 21.
- 🧠 **Credential Capture** – Detects and displays FTP `USER` and `PASS` commands sent in plaintext.
- 🚨 **Suspicious Behavior Alerts** – Tracks connection counts per IP and raises alerts when thresholds are exceeded.
- 📄 **Interactive Logging** – Optionally save logs to files after each run, avoiding unnecessary disk writes.
- 🌐 **Hostname Resolution** – Tries to resolve destination IPs to readable hostnames.

 How It Works

- Uses `scapy` to sniff network traffic on a specified interface.
- Filters for packets on TCP port 21 (standard FTP).
- Every packet is inspected:
  - If it contains FTP commands (`USER`, `PASS`), they are parsed and printed.
  - Logs every connection from a source IP to track session count.
  - If an IP exceeds a defined connection threshold (default: 5), an alert is triggered.
- All output is printed live to the terminal.
- At the end of the session, the user is prompted to optionally save logs.

 Use Cases

Here’s where `ftp_analyzer` shines:

-  **CTF challenges** – Capture credentials during a misconfigured FTP service.
-  **Internal Network Audits** – Check for insecure FTP traffic in corp networks.
-  **Lab Monitoring** – Run in a test environment to see how protocols behave.
-  **Educational Use** – Great for learning how sniffers, packet analyzers, and FTP work.
-  Not for intercepting secure protocols (FTP over TLS is not parsed).

---


Installation & Setup
You can install and run ftp_analyzer in just a few steps:

Requirements
Python 3.7+
scapy library
A system with network interface access (Linux, macOS, WSL, or Kali recommended)

Step 1: Clone the Repository
git clone https://github.com/KDh3h3/ftp_analyzer.git
cd ftp_analyzer

Step 2: Install Dependencies
pip install -r requirements.txt
If pip is not installed:
sudo apt install python3-pip -y  # Debian/Kali

Step 3: Run the Tool (as root/admin)
Use sudo because sniffing requires elevated privileges:
sudo python3 ftp_analyzer.py -i <interface>
Replace <interface> with your system's active network interface:
Example: 
lo → for localhost (good for testing with local FTP)
eth0, wlan0, etc. → for wired/wireless sniffing

Example for Localhost Testing:
sudo python3 ftp_analyzer.py -i lo
Then, in another terminal:
ftp 127.0.0.1
Use any dummy credentials — the tool will sniff them and print to screen.

Example Output

[2025-06-01 16:22:40] FTP connection from 192.168.1.10 to 192.168.1.1 (router.local)
[2025-06-01 16:22:41] FTP Username: admin (from 192.168.1.10)
[2025-06-01 16:22:42] FTP Password: 123456 (from 192.168.1.10)
[ALERT - 2025-06-01 16:22:45] Unusual FTP traffic from 192.168.1.10 – 6 connections

Stopping the Tool
Press Ctrl + C at any time to stop.
You'll be asked:
Do you want to save logs to file? [y/N]:
If you choose y, logs will be saved as:
ftp_traffic.log
ftp_alerts.log


Ethical Disclaimer
This tool is for educational and authorized use only.
