# Projeto da Disciplina de Desenvolvimento de Software

## Sobre o Projeto

Este projeto foi desenvolvido para a disciplina **Desenvolvimento de Software**, ministrada pelo **Prof. Pimenta**, durante o semestre **2026/1**.

O sistema realiza a conversão de textos em música. O texto informado pelo usuário é interpretado caractere por caractere, transformado em eventos musicais e posteriormente convertido para um arquivo **MIDI**, que pode ser reproduzido ou salvo.

Além da API desenvolvida em Flask, o projeto possui uma interface Web para facilitar a utilização das funcionalidades.

---

# Arquitetura do Projeto

```
Trabalho_Final
   |
   ├──   Projeto/
   |         ├── API.py
   |         ├── MusicGenerator.py
   |         ├── MusicInterpreter.py
   |         ├── MusicPlayer.py
   |         ├── SaveAudio.py
   |         ├── Settings.py
   |         ├── Text.py
   |         ├── Voice.py
   |         ├── faixa_gerada.mid
   ├── Frontend/
   |         ├── index.html
   |         ├── style.css
   |         └── script.js
```

---

# Tecnologias Utilizadas

- Python 3
- Flask
- Flask-CORS
- Flasgger (Swagger)
- Mido
- Tkinter
- HTML5
- CSS3
- JavaScript

---

# Pré-requisitos

Antes de executar o projeto é necessário possuir instalado:

- Python 3.10 ou superior;
- pip;
- Timidity (para reprodução MIDI em Linux).

## Instalação do Timidity (Linux)

Ubuntu/Debian:

```bash
sudo apt update
sudo apt install timidity
```

Verifique a instalação:

```bash
timidity --version
```

---

# Instalação das Dependências

Clone o repositório:

```bash
git clone (https://github.com/LeonardoSilveira-BR/Desenvolvimento-De-Software.git)
```

Entre na pasta do projeto:

```bash
cd Desenvolvimento-De-Software/Projeto
```

Instale as dependências:

```bash
pip install flask
pip install flask-cors
pip install flasgger
pip install mido
```

---

# Como Executar

Inicie a API:

      ```bash
      python API.py
      ```
      
      A API ficará disponível em:
      
      ```
      http://localhost:5000
      ```
      
      Em seguida, abra o arquivo:
      
      ```
      Frontend/index.html
      ```
      
      em um navegador.
      
      ---

# Fluxo de Funcionamento

      ```
      Texto
         │
         ▼
      MusicInterpreter
         │
         ▼
      Eventos Musicais
         │
         ▼
      MusicGenerator
         │
         ▼
      Arquivo MIDI
         │
         ▼
      MusicPlayer
      ```

---

# Endpoints da API

## Texto

| Método | Endpoint | Descrição |
|---------|----------|-----------|
| GET | /Text | Retorna o texto atual |
| PUT | /Text | Atualiza o texto |
| DELETE | /Text | Limpa o texto |
| POST | /Text/Load | Carrega arquivo TXT |

---

## Configurações

| Método | Endpoint |
|---------|----------|
| GET | /Settings |
| PUT | /Settings |

---

## Vozes

| Método | Endpoint |
|---------|----------|
| GET | /Voice |
| GET | /Voice/{id} |
| PUT | /Voice/{id} |

---

## Interpretação Musical

| Método | Endpoint |
|---------|----------|
| POST | /MusicInterpreter/Parse |
| GET | /MusicInterpreter/Events |

---

## Geração MIDI

| Método | Endpoint |
|---------|----------|
| POST | /MusicGenerator/Generate |
| GET | /MusicGenerator/Download |

---

## Reprodução

| Método | Endpoint |
|---------|----------|
| POST | /MusicPlayer/Play |
| POST | /MusicPlayer/Pause |
| POST | /MusicPlayer/Resume |
| POST | /MusicPlayer/Stop |
| POST | /MusicPlayer/Restart |
| POST | /MusicPlayer/End |
| GET | /MusicPlayer/Status |

---

**Professor:** Pimenta

**Semestre:** 2026/1
