﻿#!/usr/bin/env python3

from scapy.all import sniff, TCP, IP
import re
import socket
from datetime import datetime
import argparse

# === Configuration ===
FTP_PORT = 21
SUSPICIOUS_THRESHOLD = 5  # Max FTP sessions per IP
session_counter = {}
event_log = []
alert_log = []

# === Resolve hostname (optional) ===
def resolve_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return "Unknown"

# === Log and Print Events ===
def log_event(message):
    timestamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(timestamped)
    event_log.append(timestamped)

def alert(message):
    timestamped = f"[ALERT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    print(timestamped)
    alert_log.append(timestamped)

# === FTP Credential Sniffer ===
def sniff_credentials(payload):
    user_match = re.search(r'USER\s+(\S+)', payload)
    pass_match = re.search(r'PASS\s+(\S+)', payload)
    creds = []
    if user_match:
        creds.append(f"FTP Username: {user_match.group(1)}")
    if pass_match:
        creds.append(f"FTP Password: {pass_match.group(1)}")
    return creds

# === Packet Handler ===
def monitor_ftp(pkt):
    if pkt.haslayer(TCP) and pkt[TCP].dport == FTP_PORT:
        src_ip = pkt[IP].src
        dst_ip = pkt[IP].dst
        dst_hostname = resolve_hostname(dst_ip)

        log_event(f"FTP connection from {src_ip} to {dst_ip} ({dst_hostname})")

        session_counter[src_ip] = session_counter.get(src_ip, 0) + 1
        if session_counter[src_ip] > SUSPICIOUS_THRESHOLD:
            alert(f"Unusual FTP traffic from {src_ip} – {session_counter[src_ip]} connections")

        payload = str(bytes(pkt[TCP].payload))
        creds = sniff_credentials(payload)
        for c in creds:
            log_event(f"{c} (from {src_ip})")

# === Ask to Save Logs ===
def save_logs():
    choice = input("\nDo you want to save logs to file? [y/N]: ").strip().lower()
    if choice == 'y':
        with open("ftp_traffic.log", "w") as f:
            f.write("\n".join(event_log))
        with open("ftp_alerts.log", "w") as f:
            f.write("\n".join(alert_log))
        print("Logs saved to ftp_traffic.log and ftp_alerts.log")
    else:
        print("Logs not saved.")

# === Start Sniffing ===
def start_sniffing(interface):
    print(f"\n Monitoring FTP traffic on interface '{interface}', port {FTP_PORT}...\nPress Ctrl+C to stop.\n")
    try:
        sniff(iface=interface, filter=f"tcp port {FTP_PORT}", prn=monitor_ftp, store=0)
    except KeyboardInterrupt:
        pass
    finally:
        print("\nSniffing stopped.")
        save_logs()


# === Main Entry Point ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FTP Traffic Analyzer Tool")
    parser.add_argument("-i", "--interface", help="Network interface to sniff on", required=True)
    args = parser.parse_args()
    start_sniffing(args.interface)
