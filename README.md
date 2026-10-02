Aqui está uma estrutura de **`README.md`** completa, profissional e pronta para publicação no seu repositório do GitHub (`recon-pulse`).

Ela já vem configurada com badges, seções bem estruturadas, arquitetura do projeto, exemplos de execução reais baseados nos seus testes, screenshots, instrução de instalação com suporte a `venv` / PEP 668 e avisos legais.

---

```markdown
# ⚡ ReconPulse - Active Reconnaissance & Network Mapping Automator

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Kali-lightgrey.svg)](https://www.kali.org/)
[![Nmap Framework](https://img.shields.io/badge/engine-Nmap-red.svg)](https://nmap.org/)

**ReconPulse** é uma ferramenta em Python desenvolvida para automação, padronização e aceleração da fase de **reconhecimento ativo** e **mapeamento de superfície de ataque** em testes de invasão e auditorias de segurança de rede.

A ferramenta orquestra varreduras de rede utilizando a engine do **Nmap**, realiza o parsing estruturado das respostas, correlaciona automaticamente serviços/versões com a base local do **Exploit-DB (`searchsploit`)** e gera relatórios em **JSON** e **Markdown** prontos para documentação técnica.

---

## 🎯 Principais Funcionalidades

- **Perfis de Varredura Modulares:** Perfis pré-configurados (`quick`, `full`, `vuln`, `stealth`) ajustados para diferentes cenários de engajamento.
- **Perfil Furtivo (Evasion & Stealth):** Utilização de técnicas de evasão de IDS/Firewall (fragmentação `-f`, spoofing de porta de origem `-g 53`, adição de payload `--data-length` e timing `T2`).
- **Mapeamento de Vulnerabilidades / Exploit-DB:** Correlação automatizada de banners de serviços e versões com exploits conhecidos via `searchsploit`.
- **Parsing Estruturado:** Extração e normalização dos outputs do Nmap em objetos Python manipuláveis.
- **Interface Terminal Estilizada:** Exibição tabular interativa e colorida no terminal via biblioteca `rich`.
- **Exportação Multi-Formato:** Geração automática de relatórios estruturados em **JSON** (para ingestão em SIEMs/pipelines) e **Markdown** (para documentação no Obsidian/Notion/GitHub).

---

## 🏗️ Arquitetura do Projeto

```text
recon-pulse/
├── config/
│   └── profiles.json       # Configuração e argumentos dos perfis de scan
├── core/
│   ├── __init__.py
│   ├── scanner.py          # Módulo de execução e interface com o Nmap
│   ├── parser.py           # Parsing do resultado XML/Estruturado
│   ├── cve_search.py       # Módulo de correlação com Exploit-DB (searchsploit)
│   └── reporter.py         # Módulo de geração de relatórios (JSON / Markdown)
├── reports/                # Diretório de saída dos relatórios gerados
├── recon.py                # Entry point / CLI da aplicação
├── requirements.txt        # Dependências Python do projeto
└── README.md               # Documentação técnica do repositório

```

---

## ⚙️ Pré-requisitos do Sistema

Como o ReconPulse realiza varreduras de rede avançadas (utilizando *raw sockets* para TCP SYN stealth scans e fragmentação de pacotes) e consulta a base do Exploit-DB, os seguintes pacotes do sistema operacional são necessários:

* **Sistema Operacional:** Kali Linux, Debian, Ubuntu ou derivado Linux.
* **Python:** Versão 3.10 ou superior.
* **Nmap:** Instalado no SO (`sudo apt install nmap`).
* **Exploit-DB / Searchsploit (Opcional para `--cve`):** Instalado e atualizado (`sudo apt install exploitdb`).

---

## 🚀 Instalação e Configuração

Devido às diretivas recentes de gerenciamento de pacotes no Kali Linux (PEP 668), é recomendado instalar as dependências em um **Ambiente Virtual (`venv`)**.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/SEU_USUARIO/recon-pulse.git](https://github.com/SEU_USUARIO/recon-pulse.git)
cd recon-pulse

```

### 2. Criar e Ativar o Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Instalar Dependências Python

```bash
pip install -r requirements.txt

```

> **Nota:** Caso o comando `pip` apresente erro de certificado em redes com proxy/inspeção SSL, execute:
> ```bash
> pip install -r requirements.txt --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org
> 
> ```
> 
> 

---

## 💻 Modo de Uso

O script principal `recon.py` aceita argumentos via linha de comando para definição de alvo, perfil de execução e integração com o Exploit-DB.

### Opções da CLI

```text
usage: recon.py [-h] -t TARGET [-p {quick,full,vuln,stealth}] [-o {json,md,all}] [--cve]

ReconPulse - Automação de Reconhecimento Ativo

options:
  -h, --help            Exibe esta mensagem de ajuda
  -t TARGET, --target TARGET
                        Alvo da varredura (IP, bloco CIDR ou Domínio)
  -p {quick,full,vuln,stealth}, --profile {quick,full,vuln,stealth}
                        Perfil de Scan (Padrão: quick)
  -o {json,md,all}, --output {json,md,all}
                        Formato de exportação do relatório (Padrão: all)
  --cve                 Executa busca automatizada no Exploit-DB (searchsploit)

```

---

## 🧪 Exemplos de Execução

### 1. Varredura Rápida (Quick Scan)

```bash
sudo ./venv/bin/python recon.py -t 192.168.1.1 -p quick

```

### 2. Varredura Completa com Mapeamento de Exploits (`--cve`)

Varredura completa de todas as portas (`-p-`), detecção de serviço/versão, fingerprint de S.O. e busca automática por exploits no Exploit-DB:

```bash
sudo ./venv/bin/python recon.py -t 10.0.2.3 -p full --cve -o all

```

### 3. Varredura Furtiva (Stealth Mode)

Executa técnicas de evasão de firewall/IDS com fragmentação de pacotes e timing ajustado:

```bash
sudo ./venv/bin/python recon.py -t 10.0.2.3 -p stealth

```

---

## 📊 Perfis de Varredura Disponíveis

| Perfil | Argumentos Nmap | Descrição / Caso de Uso |
| --- | --- | --- |
| **`quick`** | `-sS -F --open` | Varredura rápida de SYN nas 100 portas mais comuns. |
| **`full`** | `-sS -sV -sC -O -p- --open` | Varredura completa em 65.535 portas com detecção de versão, SO e scripts padrão. |
| **`vuln`** | `-sV --script=vuln` | Identificação de serviço e execução da suíte de scripts de vulnerabilidade NSE. |
| **`stealth`** | `-sS -Pn -f -g 53 --data-length 16 -T2 --randomize-hosts --open` | Varredura com evasão de IDS/Firewall (fragmentação, porta de origem 53 e timing lento). |

---

## 📸 Demonstração e Resultados

### Tabela Interativa no Terminal

Execução do scan em um ambiente de laboratório vulnerável (Metasploitable) exibindo a validação de serviços e exploits correlacionados:

### Relatório Gerado em Markdown

Estrutura limpa gerada automaticamente na pasta `reports/`, pronta para inclusão em documentações técnicas:

| Porta | Protocolo | Serviço | Versão | Exploits Encontrados |
| --- | --- | --- | --- | --- |
| 21 | tcp | ftp | vsftpd 2.3.4 | 1 exploit(s) |
| 22 | tcp | ssh | OpenSSH 4.7p1 | 0 exploit(s) |
| 139 | tcp | netbios-ssn | Samba smbd 3.0.20-Debian | 1 exploit(s) |

---

## ⚠️️ Disclaimer Legal

Esta ferramenta foi desenvolvida exclusivamente para fins educacionais, testes de segurança autorizados (Red Teaming / Pentest) e auditorias de infraestrutura própria. O uso desta ferramenta contra alvos sem autorização prévia e expressa do proprietário do sistema é estritamente proibido e pode violar leis locais e internacionais de cibersegurança. Os desenvolvedores não se responsabilizam pelo uso indevido do software.

---

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo [LICENSE](https://www.google.com/search?q=LICENSE) para obter mais detalhes.

```

```
