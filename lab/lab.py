from scapy.all import *


def packet_callback(packet):
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        data = packet[Raw].load

        if dst_port == 25565:
            print(f"To {dst_ip}:{dst_port} Data: {data}")


sniff(filter="tcp", prn=packet_callback)
