import argparse
from core.scanner import ReconScanner
from core.parser import ScanParser
from core.reporter import Reporter
from rich.console import Console
from rich.table import Table

console = Console()

def main():
    parser = argparse.ArgumentParser(description="ReconPulse - Automação de Reconhecimento Ativo")
    parser.add_argument("-t", "--target", required=True, help="Alvo (IP, Range CIDR ou Domínio)")
    
    # Adicionada a opção "stealth" ao choices
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
        reporter = Reporter(parsed)
        if args.output in ["json", "all"]:
            json_file = reporter.export_json()
            console.print(f"[green][+][/green] Relatório JSON salvo em: {json_file}")
            
        if args.output in ["md", "all"]:
            md_file = reporter.export_markdown()
            console.print(f"[green][+][/green] Relatório Markdown salvo em: {md_file}")

if __name__ == "__main__":
    main()
