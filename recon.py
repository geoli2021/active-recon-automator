import argparse
from core.scanner import ReconScanner
from core.parser import ScanParser
from core.reporter import Reporter
from rich.console import Console
from rich.table import Table

console = Console()

def display_summary(parsed_data):
    """Exibe os resultados da varredura diretamente no terminal em uma tabela estilizada."""
    for host in parsed_data:
        title = f"Resultados para {host['ip']}"
        if host.get('hostname'):
            title += f" ({host['hostname']})"
            
        table = Table(title=title, show_header=True, header_style="bold magenta")
        table.add_column("Porta", style="cyan", justify="right")
        table.add_column("Proto", style="dim")
        table.add_column("Serviço", style="green")
        table.add_column("Versão", style="yellow")

        if not host['ports']:
            table.add_row("-", "-", "Nenhuma porta aberta encontrada", "-")
        else:
            for p in host['ports']:
                product = p.get('product', '')
                version = p.get('version', '')
                version_str = f"{product} {version}".strip() or "N/A"
                
                table.add_row(
                    str(p['port']),
                    p['protocol'],
                    p['service'],
                    version_str
                )

        console.print(table)
        console.print()  # Linha em branco entre hosts

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
    
    args = parser.parse_args()
    
    scanner = ReconScanner(args.target)
    results = scanner.scan(profile_name=args.profile)
    
    if results:
        parsed = ScanParser(results).parse_hosts()
        
        # Exibe a tabela no terminal
        display_summary(parsed)
        
        # Gera os relatórios
        reporter = Reporter(parsed)
        if args.output in ["json", "all"]:
            json_file = reporter.export_json()
            console.print(f"[bold green][+][/bold green] Relatório JSON salvo em: [bold white]{json_file}[/bold white]")
            
        if args.output in ["md", "all"]:
            md_file = reporter.export_markdown()
            console.print(f"[bold green][+][/bold green] Relatório Markdown salvo em: [bold white]{md_file}[/bold white]")

if __name__ == "__main__":
    main()
