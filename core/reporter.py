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
        with open(filepath, "w") as f:
            json.dump(self.data, f, indent=4)
        return filepath

    def export_markdown(self, filename=None):
        filename = filename or f"recon_scan_{self.timestamp}.md"
        filepath = os.path.join(self.output_dir, filename)
        
        md_content = f"# Relatório de Reconhecimento Ativo\n"
        md_content += f"**Data:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for host in self.data:
            md_content += f"## Target: {host['ip']} ({host['hostname']})\n"
            md_content += f"- **Status:** {host['status']}\n"
            if host['os']:
                md_content += f"- **S.O. Detectado:** {', '.join(host['os'])}\n"
            
            md_content += "\n### Portas Abertas e Serviços\n\n"
            md_content += "| Porta | Protocolo | Serviço | Versão |\n"
            md_content += "|---|---|---|---|\n"  # Adicionados os separadores das colunas Serviço e Versão
            
            for p in host['ports']:
                version_str = f"{p['product']} {p['version']}".strip() or "N/A"
                md_content += f"| {p['port']} | {p['protocol']} | {p['service']} | {version_str} |\n"
                
            md_content += "\n"
            
        with open(filepath, "w") as f:
            f.write(md_content)
        return filepath
