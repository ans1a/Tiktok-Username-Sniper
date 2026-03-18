<div align="center">

```

```

## ⚡ Quick Start

```bash
# Termux (Android) — copie e cole tudo de uma vez:
pkg install python chafa git -y && git clone https://github.com/ans1a/Tiktok-Username-Sniper.git && cd Tiktok-Username-Sniper && bash install.sh && python tiktok_checker.py
```

```bash
# Linux — copie e cole tudo de uma vez:
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git && cd Tiktok-Username-Sniper && bash install.sh && python tiktok_checker.py
```

```powershell
# Windows (PowerShell):
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git; cd Tiktok-Username-Sniper; pip install -r requirements.txt; python tiktok_checker.py
```


# TikTok Username Checker

**PT** · **EN**

Checa usernames disponíveis no TikTok em tempo real, com múltiplos modos de geração, dicionário de idiomas do mundo inteiro e verificação anti-reservado  ( nao funciona muito bem ) por API.

Checks TikTok username availability in real time, with multiple generation modes, worldwide language dictionary, and API-based anti-reserved ( dont work very well ) detection.

</div>

---

## 🇧🇷 Português

### O que é isso?

Uma script em Python que gera usernames aleatórios e checa automaticamente se estão disponíveis no TikTok. Quando encontra um disponível, mostra no terminal e envia para um webhook do Discord.

### Instalação — Termux (Android)

```bash
# 1. Instalar Python e chafa
pkg install python chafa -y

# 2. Clonar o repositório
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper

# 3. Instalar dependências
bash install.sh
```

### Instalação — Linux

```bash
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
bash install.sh
```

### Instalação — Windows

```powershell
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
pip install -r requirements.txt
```

### Como usar

rode sh install.sh no termux.

```bash
python tiktok_checker.py
```

Na primeira execução a script vai perguntar:

| Passo | O que faz |
|-------|-----------|
| Idioma | Escolha Português BR ou English |
| Salvar hits | Se quer salvar usernames encontrados em `hitsusernames.txt` |
| Webhook | URL do webhook do Discord — salvo automaticamente em `tiktok.json` |
| Modo | Qual modo de geração usar |
| Range | Tamanho dos usernames (ex: `5-6`) |
| Threads | Quantas verificações em paralelo |

### Modos de geração

| Modo | Tipo | Exemplos |
|------|------|----------|
| 1 | Só letras | `bryyk` `seeys` `oyyop` `nunch` |
| 2 | Com números | `br66k` `n4n4v` `nr4h` `mx99k` |
| 3 | Combinado 3:2 | mistura dos dois acima |
| 4 | 1 num ⭐ | `ea6ts` `h0tel` `n1ght` `bl4de` |
| 5 | Dicionário mundial (contém números também)| `amor` `yuki` `stark` `notte` `dulce` |

> **Modo 4 (1 num ⭐)** é o recomendado. Gera nomes curtos e pronunciáveis com substituições leet — o tipo de username que vale dinheiro caso você queira vender no TikTok.

### Sistema de verificação

A script usa **3 camadas** para evitar falsos positivos (reportar como disponível algo que na verdade é reservado pelo TikTok):

```
1. oEmbed API          → checa se há perfil ativo
2. User Detail API     → detecta statusCode 10221 (reservado)
3. HTML check          → analisa SIGI_STATE, título da página
                         e texto "couldn't find this account"
```

Nomes como `plat0`, `obrai`, `auchw` e etc são **reservados** pelo TikTok — existem no sistema mas ninguém pode registrar. A script identifica e ignora esses casos. ( não funciona muito bem )

### Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `tiktok_checker.py` | Script principal |
| `requirements.txt` | Dependências Python |
| `install.sh` | Instalação automática |
| `tiktok.json` | Webhook salvo (gerado automaticamente) |
| `hitsusernames.txt` | Usernames disponíveis encontrados |
| `msk.jpg` | Imagem exibida no terminal (coloque você mesmo) |

### Dependências

```
requests
colorama
urllib3
PySocks
chafa (pkg — para exibir imagem no terminal)
```

### Webhook Discord

Quando um username é encontrado, a mensagem enviada é:

```
`ea6ts` available on tiktok #ea6ts ig
```

O nome fica entre backticks — no Discord você clica e já seleciona para copiar.

---

## 🇺🇸 English

### What is this?

A Python script that generates random usernames and automatically checks if they're available on TikTok. When it finds one that's free, it prints it in the terminal and fires off a Discord webhook.

### Installation — Termux (Android)

```bash
# 1. Install Python and chafa
pkg install python chafa -y

# 2. Clone the repo
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper

# 3. Install dependencies
bash install.sh
```

### Installation — Linux

```bash
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
bash install.sh
```

### Installation — Windows

```powershell
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
pip install -r requirements.txt
```

### How to use

Drop `msk.jpg` in the same folder as the script, then run:

```bash
python tiktok_checker.py
```

On first launch it'll walk you through setup:

| Step | What it does |
|------|-------------|
| Language | Pick Portuguese BR or English |
| Save hits | Whether to log found usernames to `hitsusernames.txt` |
| Webhook | Discord webhook URL — saved automatically to `tiktok.json` |
| Mode | Which generation mode to use |
| Range | Username length range (e.g. `5-6`) |
| Threads | How many concurrent checks to run |

### Generation modes

| Mode | Type | Examples |
|------|------|---------|
| 1 | Letters only | `bryyk` `seeys` `oyyop` `nunch` |
| 2 | With numbers | `br66k` `n4n4v` `nr4h` `mx99k` |
| 3 | Combined 3:2 | mix of both above |
| 4 | Rare/OG ⭐ | `ea6ts` `h0tel` `n1ght` `bl4de` |
| 5 | World dictionary | `amor` `yuki` `stark` `notte` `dulce` |

> **Mode 4 (Rare/OG)** is the recommended pick. It generates short, pronounceable names with leet substitutions — exactly the kind of username that goes for real money on TikTok.

### How the checker works

Three-layer verification to avoid false positives (marking reserved usernames as available):

```
1. oEmbed API          → checks for an active profile
2. User Detail API     → catches statusCode 10221 (reserved by TikTok)
3. HTML check          → parses SIGI_STATE, page title,
                         and "couldn't find this account" text
```

Names like `plat0`, `obrai`, and `auchw` etc are **reserved** by TikTok — they exist in the system but nobody can register them. The script detects and skips these. ( dont work very well )

### Files

| File | Description |
|------|-------------|
| `tiktok_checker.py` | Main script |
| `requirements.txt` | Python dependencies |
| `install.sh` | Auto-installer |
| `tiktok.json` | Saved webhook (auto-generated) |
| `hitsusernames.txt` | Available usernames found |
| `msk.jpg` | Image shown in terminal (add it yourself) |

### Dependencies

```
requests
colorama
urllib3
PySocks
chafa (pkg — for terminal image display)
```

### Discord webhook format

When a username is found, the message sent looks like this:

```
`ea6ts` available on tiktok #ea6ts ig
```

The name is wrapped in backticks so you can click it in Discord to instantly select and copy.

---

<div align="center">

made with 🖤

</div>
<div align="center">

```

```

## ⚡ Quick Start

```bash
# Termux (Android) — copie e cole tudo de uma vez:
pkg install python chafa git -y && git clone https://github.com/ans1a/Tiktok-Username-Sniper.git && cd Tiktok-Username-Sniper && bash install.sh && python tiktok_checker.py
```

```bash
# Linux — copie e cole tudo de uma vez:
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git && cd Tiktok-Username-Sniper && bash install.sh && python tiktok_checker.py
```

```powershell
# Windows (PowerShell):
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git; cd Tiktok-Username-Sniper; pip install -r requirements.txt; python tiktok_checker.py
```


# TikTok Username Checker

**PT** · **EN**

Checa usernames disponíveis no TikTok em tempo real, com múltiplos modos de geração, dicionário de idiomas do mundo inteiro e verificação anti-reservado  ( nao funciona muito bem ) por API.

Checks TikTok username availability in real time, with multiple generation modes, worldwide language dictionary, and API-based anti-reserved ( dont work very well ) detection.

</div>

---

## 🇧🇷 Português

### O que é isso?

Uma script em Python que gera usernames aleatórios e checa automaticamente se estão disponíveis no TikTok. Quando encontra um disponível, mostra no terminal e envia para um webhook do Discord.

### Instalação — Termux (Android)

```bash
# 1. Instalar Python e chafa
pkg install python chafa -y

# 2. Clonar o repositório
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper

# 3. Instalar dependências
bash install.sh
```

### Instalação — Linux

```bash
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
bash install.sh
```

### Instalação — Windows

```powershell
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
pip install -r requirements.txt
```

### Como usar

rode sh install.sh no termux.

```bash
python tiktok_checker.py
```

Na primeira execução a script vai perguntar:

| Passo | O que faz |
|-------|-----------|
| Idioma | Escolha Português BR ou English |
| Salvar hits | Se quer salvar usernames encontrados em `hitsusernames.txt` |
| Webhook | URL do webhook do Discord — salvo automaticamente em `tiktok.json` |
| Modo | Qual modo de geração usar |
| Range | Tamanho dos usernames (ex: `5-6`) |
| Threads | Quantas verificações em paralelo |

### Modos de geração

| Modo | Tipo | Exemplos |
|------|------|----------|
| 1 | Só letras | `bryyk` `seeys` `oyyop` `nunch` |
| 2 | Com números | `br66k` `n4n4v` `nr4h` `mx99k` |
| 3 | Combinado 3:2 | mistura dos dois acima |
| 4 | 1 num ⭐ | `ea6ts` `h0tel` `n1ght` `bl4de` |
| 5 | Dicionário mundial (contém números também)| `amor` `yuki` `stark` `notte` `dulce` |

> **Modo 4 (1 num ⭐)** é o recomendado. Gera nomes curtos e pronunciáveis com substituições leet — o tipo de username que vale dinheiro caso você queira vender no TikTok.

### Sistema de verificação

A script usa **3 camadas** para evitar falsos positivos (reportar como disponível algo que na verdade é reservado pelo TikTok):

```
1. oEmbed API          → checa se há perfil ativo
2. User Detail API     → detecta statusCode 10221 (reservado)
3. HTML check          → analisa SIGI_STATE, título da página
                         e texto "couldn't find this account"
```

Nomes como `plat0`, `obrai`, `auchw` e etc são **reservados** pelo TikTok — existem no sistema mas ninguém pode registrar. A script identifica e ignora esses casos. ( não funciona muito bem )

### Arquivos

| Arquivo | Descrição |
|---------|-----------|
| `tiktok_checker.py` | Script principal |
| `requirements.txt` | Dependências Python |
| `install.sh` | Instalação automática |
| `tiktok.json` | Webhook salvo (gerado automaticamente) |
| `hitsusernames.txt` | Usernames disponíveis encontrados |
| `msk.jpg` | Imagem exibida no terminal (coloque você mesmo) |

### Dependências

```
requests
colorama
urllib3
PySocks
chafa (pkg — para exibir imagem no terminal)
```

### Webhook Discord

Quando um username é encontrado, a mensagem enviada é:

```
`ea6ts` available on tiktok #ea6ts ig
```

O nome fica entre backticks — no Discord você clica e já seleciona para copiar.

---

## 🇺🇸 English

### What is this?

A Python script that generates random usernames and automatically checks if they're available on TikTok. When it finds one that's free, it prints it in the terminal and fires off a Discord webhook.

### Installation — Termux (Android)

```bash
# 1. Install Python and chafa
pkg install python chafa -y

# 2. Clone the repo
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper

# 3. Install dependencies
bash install.sh
```

### Installation — Linux

```bash
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
bash install.sh
```

### Installation — Windows

```powershell
git clone https://github.com/ans1a/Tiktok-Username-Sniper.git
cd Tiktok-Username-Sniper
pip install -r requirements.txt
```

### How to use

Drop `msk.jpg` in the same folder as the script, then run:

```bash
python tiktok_checker.py
```

On first launch it'll walk you through setup:

| Step | What it does |
|------|-------------|
| Language | Pick Portuguese BR or English |
| Save hits | Whether to log found usernames to `hitsusernames.txt` |
| Webhook | Discord webhook URL — saved automatically to `tiktok.json` |
| Mode | Which generation mode to use |
| Range | Username length range (e.g. `5-6`) |
| Threads | How many concurrent checks to run |

### Generation modes

| Mode | Type | Examples |
|------|------|---------|
| 1 | Letters only | `bryyk` `seeys` `oyyop` `nunch` |
| 2 | With numbers | `br66k` `n4n4v` `nr4h` `mx99k` |
| 3 | Combined 3:2 | mix of both above |
| 4 | Rare/OG ⭐ | `ea6ts` `h0tel` `n1ght` `bl4de` |
| 5 | World dictionary | `amor` `yuki` `stark` `notte` `dulce` |

> **Mode 4 (Rare/OG)** is the recommended pick. It generates short, pronounceable names with leet substitutions — exactly the kind of username that goes for real money on TikTok.

### How the checker works

Three-layer verification to avoid false positives (marking reserved usernames as available):

```
1. oEmbed API          → checks for an active profile
2. User Detail API     → catches statusCode 10221 (reserved by TikTok)
3. HTML check          → parses SIGI_STATE, page title,
                         and "couldn't find this account" text
```

Names like `plat0`, `obrai`, and `auchw` etc are **reserved** by TikTok — they exist in the system but nobody can register them. The script detects and skips these. ( dont work very well )

### Files

| File | Description |
|------|-------------|
| `tiktok_checker.py` | Main script |
| `requirements.txt` | Python dependencies |
| `install.sh` | Auto-installer |
| `tiktok.json` | Saved webhook (auto-generated) |
| `hitsusernames.txt` | Available usernames found |
| `msk.jpg` | Image shown in terminal (add it yourself) |

### Dependencies

```
requests
colorama
urllib3
PySocks
chafa (pkg — for terminal image display)
```

### Discord webhook format

When a username is found, the message sent looks like this:

```
`ea6ts` available on tiktok #ea6ts ig
```

The name is wrapped in backticks so you can click it in Discord to instantly select and copy.

---

<div align="center">

made with 🖤

</div>
