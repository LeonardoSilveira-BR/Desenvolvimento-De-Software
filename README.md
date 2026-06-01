# Projeto da Disciplina de Desenvolvimento de Software

## Sobre o Projeto

Este projeto foi desenvolvido para a disciplina de **Desenvolvimento de Software**, ministrada pelo **Prof. Pimenta**, no semestre **2026/1**.

O sistema permite converter textos em música por meio de regras de interpretação musical. O texto é analisado caractere por caractere, transformado em eventos musicais e posteriormente convertido para um arquivo MIDI que pode ser reproduzido ou salvo pelo usuário.

---

## Funcionalidades

- Carregar textos a partir de arquivos `.txt`;
- Inserir textos manualmente;
- Interpretar textos como eventos musicais;
- Configurar BPM, volume e instrumentos;
- Gerar arquivos MIDI;
- Reproduzir, pausar e parar a música gerada;
- Salvar o arquivo MIDI gerado.

---

## Estrutura do Projeto

| Arquivo | Responsabilidade |
|----------|------------------|
| `Text.py` | Leitura e armazenamento de textos |
| `Voice.py` | Representação das vozes musicais |
| `Settings.py` | Configurações de BPM, volume e instrumentos |
| `MusicInterpreter.py` | Conversão do texto em eventos musicais |
| `MusicGenerator.py` | Geração do arquivo MIDI |
| `MusicPlayer.py` | Reprodução do arquivo MIDI |
| `SaveAudio.py` | Salvamento do arquivo MIDI |
| `API.py` | Disponibilização das funcionalidades através de uma API REST |

---

## Tecnologias Utilizadas

- Python 3
- Flask
- Flask-CORS
- Flasgger (Swagger)
- Mido
- Pygame
- Tkinter

---

## Como Executar

### Instalar dependências

```bash
pip install flask
pip install flask-cors
pip install flasgger
pip install pygame
pip install mido
```

### Executar a API

```bash
python API.py
```

A aplicação ficará disponível em:

```text
http://localhost:5000
```

---

## Principais Endpoints

### Texto

```http
GET /Text
PUT /Text
POST /Text/Load
```

### Configurações

```http
GET /Settings
PUT /Settings
```

### Vozes

```http
GET /Voice
GET /Voice/{id}
PUT /Voice/{id}
```

### Interpretação Musical

```http
POST /MusicInterpreter/Parse
GET /MusicInterpreter/Events
```

### Geração MIDI

```http
POST /MusicGenerator/Generate
GET /MusicGenerator/Download
```

### Reprodução

```http
POST /MusicPlayer/Play
POST /MusicPlayer/Pause
POST /MusicPlayer/Resume
POST /MusicPlayer/Stop
POST /MusicPlayer/Restart
POST /MusicPlayer/End
GET  /MusicPlayer/Status
```

---

## Fluxo de Funcionamento

```text
Texto
  ↓
MusicInterpreter
  ↓
Eventos Musicais
  ↓
MusicGenerator
  ↓
Arquivo MIDI
  ↓
MusicPlayer
```

---

## Disciplina

**Desenvolvimento de Software**  
Professor Pimenta  
Semestre 2026/1
