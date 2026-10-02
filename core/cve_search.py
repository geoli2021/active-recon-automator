import subprocess
import json
import logging

class CVEMapper:
    def __init__(self, timeout=10):
        self.timeout = timeout
        # Termos genéricos ou versões curtas que causam ruído no searchsploit
        self.ignored_versions = {"1", "2", "3", "v1", "v2", "1.0", "2.0", "3.0", "N/A", "unknown"}

    def _is_valid_query(self, service, version):
        """
        Valida se os termos de busca possuem precisão suficiente para evitar falsos positivos.
        """
        if not service or not version:
            return False
            
        version_clean = version.strip().lower()
        
        # Ignora versões muito curtas ou genéricas (ex: versão "1" do serviço rpcbind/status)
        if version_clean in self.ignored_versions or len(version_clean) < 3:
            return False
            
        return True

    def search_exploits(self, service_name, version):
        """
        Consulta a base do searchsploit local buscando exploits associados ao serviço/versão.
        """
        if not self._is_valid_query(service_name, version):
            return []

        # Concatena o nome do produto/serviço com a versão específica (ex: "vsftpd 2.3.4")
        query = f"{service_name} {version}".strip()
        
        try:
            # Executa o searchsploit nativo com saída estruturada em JSON
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
                
                # Extrai os dados relevantes dos resultados
                for item in data.get("RESULTS_EXPLOIT", []):
                    exploits.append({
                        "title": item.get("Title"),
                        "edb_id": item.get("EDB-ID"),
                        "type": item.get("Type"),
                        "platform": item.get("Platform")
                    })
                return exploits

        except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
            logging.debug(f"Falha ao consultar searchsploit para '{query}': {e}")
            
        return []

    def enrich_parsed_data(self, parsed_hosts):
        """
        Percorre a lista de hosts e portas adicionando a lista de exploits correlacionados.
        """
        for host in parsed_hosts:
            for port in host.get("ports", []):
                service = port.get("service", "")
                product = port.get("product", "")
                version = port.get("version", "")
                
                # Prioriza o nome do produto específico (ex: 'vsftpd') em vez do serviço genérico (ex: 'ftp')
                query_service = product if product else service
                
                exploits = self.search_exploits(query_service, version)
                port["known_exploits"] = exploits
                
        return parsed_hosts
