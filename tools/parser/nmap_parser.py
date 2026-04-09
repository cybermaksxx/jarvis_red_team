#!/usr/bin/env python3
import xmltodict

def parse_nmap(xml_file: str) -> list:
    # open and read file
    with open(xml_file, "r") as f:
        raw = f.read()

    # making xml a dictionary
    data = xmltodict.parse(raw)

    # going in depth of dict to host 
    hosts = data["nmaprun"]["host"]

    
    if isinstance(hosts, dict):
        hosts = [hosts]

    results = []

    for host in hosts:
        # getting an ip adress
        address = host["address"]
        if isinstance(address, list):
            address = address[0]  # берём первый адрес — это IPv4
        ip = address["@addr"]

        # going to the ports
        ports = host["ports"]["port"]

        # it should always be dict
        if isinstance(ports, dict):
            ports = [ports]

        for port in ports:
            # only open ports is used
            if port["state"]["@state"] == "open":

                # .get() — secure
                service = port.get("service", {})

                result = {
                    "host": ip,
                    "port": int(port["@portid"]),
                    "protocol": port["@protocol"],
                    "service": service.get("@name", "unknown"),
                    "version": service.get("@version", ""),
                    "state": "open"
                }

                results.append(result)

    return results


if __name__ == "__main__":
    results = parse_nmap("output.xml")

    for r in results:
        print(f"{r['host']} | {r['port']}/{r['protocol']} | {r['service']} | {r['version']}")
