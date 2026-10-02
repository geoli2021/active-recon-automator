import nmap
import json
import os
from rich.console import Console

console = Console()

class ReconScanner:
    def __init__(self, target, profiles_path="config/profiles.json"):
        self.target = target
        self.nm = nmap.PortScanner()
        self.profiles = self._load_profiles(profiles_path)

    def _load_profiles(self, path):
        if not os.path.exists(path):
            # Perfis padrão caso o arquivo não exista
            return {
                "quick": "-sS -F --open",
                "full": "-sS -sV -sC -O -p- --open",
                "vuln": "-sV --script=vuln"
            }
        with open(path, "r") as f:
            return json.load(f)

    def scan(self, profile_name="quick", custom_args=None):
        arguments = custom_args if custom_args else self.profiles.get(profile_name, "-sS -F")
        console.print(f"[bold blue][*][/bold blue] Iniciando scan em [bold green]{self.target}[/bold green] com perfil [yellow]{profile_name}[/yellow]...")
        console.print(f"[dim]Argumentos Nmap: {arguments}[/dim]\n")
        
        try:
            self.nm.scan(hosts=self.target, arguments=arguments)
            return self.nm
        except Exception as e:
            console.print(f"[bold red][!] Erro na execução do Nmap:[/bold red] {e}")
            return None
