import subprocess
import json
import logging

class CVEMapper:
    def __init__(self, timeout=10):
        self.timeout = timeout

    def search_exploits(self, service_name, version):
        """
        Consulta a base do searchsploit local buscando exploits associados ao serviço/versão.
        """
        if not service_name or not version or version == "N/A":
            return []

        # Limpa e prepara a string de busca (ex: "vsftpd 2.3.4")
        query = f"{service_name} {version}".strip()
        
        try:
            # Executa o searchsploit nativo com saída em formato JSON
            cmd = ["searchsploit", "--json", query]
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )

            if result.returncode == 0 and result.stdout:
                data = json.loads(result.stdout)
                exploits = []
                
                # Extrai os títulos e caminhos dos exploits encontrados
                for item in data.get("RESULTS_EXPLOIT", []):
                    exploits.append({
                        "title": item.get("Title"),
                        "edb_id": item.get("EDB-ID"),
                        "type": item.get("Type"),
                        "platform": item.get("Platform")
                    })
                return exploits

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
            # Se o searchsploit não estiver instalado ou falhar, retorna lista vazia de forma graciosa
            logging.debug(f"Falha ao consultar searchsploit para {query}: {e}")
            
        return []

    def enrich_parsed_data(self, parsed_hosts):
        """
        Percorre a estrutura de hosts e portas adicionando a lista de exploits encontrados.
        """
        for host in parsed_hosts:
            for port in host.get("ports", []):
                service = port.get("service", "")
                product = port.get("product", "")
                version = port.get("version", "")
                
                # Prioriza o nome do produto (ex: 'vsftpd') sobre o nome genérico do serviço (ex: 'ftp')
                query_service = product if product else service
                
                exploits = self.search_exploits(query_service, version)
                port["known_exploits"] = exploits
                
        return parsed_hosts
