import argparse
from core.scanner import ReconScanner
from core.parser import ScanParser
from core.reporter import Reporter
from core.cve_search import CVEMapper
from rich.console import Console
from rich.table import Table

console = Console()

def display_summary(parsed_data, show_cve=False):
    for host in parsed_data:
        title = f"Resultados para {host['ip']}"
        if host.get('hostname'):
            title += f" ({host['hostname']})"
            
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Porta", style="cyan", justify="right")
        table.add_column("Proto", style="dim")
        table.add_column("Serviço", style="green")
        table.add_column("Versão", style="yellow")
        if show_cve:
            table.add_column("Exploits DB", style="red")

        if not host['ports']:
            row = ["-", "-", "Nenhuma porta aberta encontrada", "-"]
            if show_cve:
                row.append("-")
            table.add_row(*row)
        else:
            for p in host['ports']:
                product = p.get('product', '')
                version = p.get('version', '')
                version_str = f"{product} {version}".strip() or "N/A"
                
                row = [str(p['port']), p['protocol'], p['service'], version_str]
                
                if show_cve:
                    exploits = p.get('known_exploits', [])
                    row.append(f"{len(exploits)} encontrado(s)" if exploits else "0")
                    
                table.add_row(*row)

        console.print(table)
        console.print()

def main():
    parser = argparse.ArgumentParser(description="ReconPulse - Automação de Reconhecimento Ativo")
    parser.add_argument("-t", "--target", required=True, help="Alvo (IP, Range CIDR ou Domínio)")
    parser.add_argument(
        "-p", "--profile", 
        default="quick", 
        choices=["quick", "full", "vuln", "stealth"], 
        help="Perfil de Scan"
    )
    parser.add_argument("-o", "--output", default="all", choices=["json", "md", "all"], help="Formato de exportação")
    parser.add_argument("--cve", action="store_true", help="Realiza busca de exploits públicos (Exploit-DB/searchsploit)")
    
    args = parser.parse_args()
    
    scanner = ReconScanner(args.target)
    results = scanner.scan(profile_name=args.profile)
    
    if results:
        parsed = ScanParser(results).parse_hosts()
        
        # Se a flag --cve for passada, enriquece os dados com o Exploit-DB
        if args.cve:
            console.print("[bold yellow][*][/bold yellow] Consultando base local do Exploit-DB via searchsploit...")
            mapper = CVEMapper()
            parsed = mapper.enrich_parsed_data(parsed)
        
        display_summary(parsed, show_cve=args.cve)
        
        reporter = Reporter(parsed)
        if args.output in ["json", "all"]:
            json_file = reporter.export_json()
            console.print(f"[bold green][+][/bold green] Relatório JSON salvo em: [bold white]{json_file}[/bold white]")
            
        if args.output in ["md", "all"]:
            md_file = reporter.export_markdown()
            console.print(f"[bold green][+][/bold green] Relatório Markdown salvo em: [bold white]{md_file}[/bold white]")

if __name__ == "__main__":
    main()
