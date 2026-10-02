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
            
            # Cabeçalho formatado com separadores para as 4 colunas
            md_content += "| Porta | Protocolo | Serviço | Versão |\n"
            md_content += "|---|---|---|---|\n"
            
            for p in host['ports']:
                product = p.get('product', '')
                version = p.get('version', '')
                version_str = f"{product} {version}".strip() or "N/A"
                md_content += f"| {p['port']} | {p['protocol']} | {p['service']} | {version_str} |\n"
                
            md_content += "\n"
            
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
        return filepath
