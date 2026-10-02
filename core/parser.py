class ScanParser:
    def __init__(self, scanner_data):
        self.data = scanner_data

    def parse_hosts(self):
        parsed_results = []
        
        for host in self.data.all_hosts():
            host_info = {
                "ip": host,
                "hostname": self.data[host].hostname(),
                "status": self.data[host].state(),
                "os": [],
                "ports": []
            }
            
            # Detecção de S.O. se disponível
            if 'osmatch' in self.data[host]:
                for match in self.data[host]['osmatch']:
                    host_info["os"].append(match['name'])

            # Portas e Serviços
            for proto in self.data[host].all_protocols():
                ports = self.data[host][proto].keys()
                for port in ports:
                    p_info = self.data[host][proto][port]
                    
                    scripts_output = p_info.get('script', {})
                    
                    host_info["ports"].append({
                        "port": port,
                        "protocol": proto,
                        "state": p_info['state'],
                        "service": p_info['name'],
                        "product": p_info.get('product', ''),
                        "version": p_info.get('version', ''),
                        "extrainfo": p_info.get('extrainfo', ''),
                        "vulnerabilities": scripts_output
                    })
                    
            parsed_results.append(host_info)
            
        return parsed_results
