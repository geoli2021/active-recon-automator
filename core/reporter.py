import json
import os
from datetime import datetime

class Reporter:
    def __init__(self, parsed_data, output_dir="reports"):
        self.data = parsed_data
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def export_json(self, filename=None):
        filename = filename or f"recon_scan_{self.timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)
        return filepath

    def export_markdown(self, filename=None):
        filename = filename or f"recon_scan_{self.timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        md_content = f"# Relatório de Reconhecimento Ativo\n"
        md_content += f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for host in self.data:
            hostname_str = f" ({host['hostname']})" if host.get('hostname') else ""
            md_content += f"## Target: {host['ip']}{hostname_str}\n"
            md_content += f"- **Status:** {host['status']}\n"
            if host.get('os'):
                md_content += f"- **S.O. Detectado:** {', '.join(host['os'])}\n"
            
            md_content += "\n### Portas Abertas e Serviços\n\n"
            md_content += "| Porta | Protocolo | Serviço | Versão | Exploits Encontrados |\n"
            md_content += "|---|---|---|---|---|\n"
            
            for p in host['ports']:
                product = p.get('product', '')
                version = p.get('version', '')
                version_str = f"{product} {version}".strip() or "N/A"
                
                # Contagem de exploits correlacionados
                exploits = p.get('known_exploits', [])
                exploit_str = f"{len(exploits)} exploit(s)" if exploits else "Nenhum"
                
                md_content += f"| {p['port']} | {p['protocol']} | {p['service']} | {version_str} | {exploit_str} |\n"
                
            # Seção detalhada de Exploits se houver achados
            has_exploits = any(p.get('known_exploits') for p in host['ports'])
            if has_exploits:
                md_content += "\n### ⚠️ Correlação de Vulnerabilidades (Exploit-DB)\n\n"
                for p in host['ports']:
                    if p.get('known_exploits'):
                        md_content += f"#### Porta {p['port']}/{p['protocol']} - {p['service']} ({p.get('product', '')} {p.get('version', '')})\n"
                        for exp in p['known_exploits']:
                            md_content += f"- **[{exp['edb_id']}]** {exp['title']} *({exp['platform']} / {exp['type']})*\n"
                        md_content += "\n"
                        
            md_content += "\n"
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        return filepath
