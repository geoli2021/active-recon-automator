# ⚡ ReconPulse - Active Reconnaissance & Network Mapping Automator

**ReconPulse** é uma ferramenta em Python desenvolvida para automação, padronização e aceleração da fase de **reconhecimento ativo** e **mapeamento de superfície de ataque** em auditorias de segurança de rede.

A ferramenta orquestra varreduras de rede utilizando a engine do **Nmap**, realiza o parsing estruturado das respostas, correlaciona serviços/versões com a base do **Exploit-DB (searchsploit)** e gera relatórios em **JSON** e **Markdown**.

---

## 🎯 Principais Funcionalidades

- **Perfis de Varredura Modulares:** Perfis pré-configurados (quick, full, vuln, stealth) ajustados para diferentes cenários de engajamento.
- **Perfil Furtivo (Evasion & Stealth):** Utilização de técnicas de evasão de IDS/Firewall (fragmentação de pacotes, porta de origem 53, data-length e timing T2).
- **Mapeamento de Vulnerabilidades / Exploit-DB:** Correlação automatizada de banners de serviços e versões com exploits conhecidos via searchsploit.
- **Parsing Estruturado:** Extração e normalização dos outputs do Nmap em objetos Python manipuláveis.
- **Interface Terminal Estilizada:** Exibição tabular interativa e colorida no terminal via biblioteca rich.
- **Exportação Multi-Formato:** Geração automática de relatórios estruturados em JSON e Markdown.

---

## ⚙️ Pré-requisitos do Sistema

- **Sistema Operacional:** Kali Linux, Debian, Ubuntu ou derivado Linux.
- **Python:** Versão 3.10 ou superior.
- **Nmap:** Pacote nmap instalado no sistema operativo.
- **Exploit-DB:** Pacote exploitdb (searchsploit) instalado e atualizado.

---

## 🚀 Instalação e Configuração

1. Clone o repositório para a sua máquina local utilizando o Git.
2. Navegue até ao diretório do projeto.
3. Crie um ambiente virtual Python e ative-o.
4. Instale as dependências listadas no ficheiro requirements.txt através do pip.

---

## 💻 Modo de Uso

A ferramenta é executada via linha de comandos (recon.py) aceitando os seguintes parâmetros:

- **-t / --target:** Endereço IP do alvo, bloco CIDR ou domínio (obrigatório).
- **-p / --profile:** Perfil de varredura desejado (opções: quick, full, vuln, stealth. Padrão: quick).
- **-o / --output:** Formato do relatório gerado (opções: json, md, all. Padrão: all).
- **--cve:** Chave opcional que ativa a consulta automatizada à base do Exploit-DB via searchsploit.

---

## 📊 Perfis de Varredura Disponíveis

| Perfil | Argumentos Nmap | Descrição / Caso de Uso |
| :--- | :--- | :--- |
| **quick** | -sS -F --open | Varredura rápida de SYN nas 100 portas mais comuns. |
| **full** | -sS -sV -sC -O -p- --open | Varredura completa em 65.535 portas com detecção de versão, SO e scripts padrão. |
| **vuln** | -sV --script=vuln | Identificação de serviços e execução da suíte de scripts de vulnerabilidade NSE. |
| **stealth** | -sS -Pn -f -g 53 --data-length 16 -T2 --randomize-hosts --open | Varredura com evasão de IDS/Firewall (fragmentação, porta de origem 53 e timing lento). |

---

# 💻 Comandos de Instalação e Execução

# 1. Clonar o repositório
git clone https://github.com/SEU_USUARIO/recon-pulse.git
cd recon-pulse

# 2. Criar e ativar o ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Exemplo - Quick Scan
sudo ./venv/bin/python recon.py -t 192.168.1.1 -p quick

# 5. Exemplo - Full Scan com consulta ao Exploit-DB
sudo ./venv/bin/python recon.py -t 10.0.2.3 -p full --cve -o all

# 6. Exemplo - Stealth Scan (Evasão)
sudo ./venv/bin/python recon.py -t 10.0.2.3 -p stealth

---

## 📸 Demonstração e Resultados

- **Tabela Interativa no Terminal:** Exibição dos resultados com identificação de portas, serviços, versões e número de exploits encontrados.
- **Relatório Gerado em Markdown:** Ficheiro exportado automaticamente para a pasta de relatórios, pronto para inclusão em relatórios técnicos de pentest.

---

## ⚠ Disclaimer Legal

Esta ferramenta foi desenvolvida exclusivamente para fins educacionais, testes de segurança autorizados e auditorias de infraestrutura própria. O uso desta ferramenta contra alvos sem autorização prévia e expressa é estritamente proibido. Os desenvolvedores não se responsabilizam pelo uso indevido do software.

---

## 📜 Licença

Este projeto está licenciado sob a Licença MIT.
