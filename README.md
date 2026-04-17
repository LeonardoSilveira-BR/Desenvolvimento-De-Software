# 🎵 Gerador de Música a partir de Texto

Projeto desenvolvido para a disciplina **INF01120 - Técnicas de Construção de Programas**  
Universidade Federal do Rio Grande do Sul (UFRGS)  
Professor: Marcelo Soares Pimenta

---

# 📌 Descrição do Projeto

Este projeto implementa um **Gerador de Música a partir de Texto**.  
O sistema lê um texto e converte os caracteres em **notas musicais**, permitindo:

- gerar som automaticamente
- salvar a música gerada em **arquivo MIDI**

Nesta **Fase 2**, foram adicionadas novas funcionalidades e mudanças importantes no mapeamento do texto para música, permitindo gerar estruturas musicais inspiradas em **fugas de Johann Sebastian Bach**, utilizando múltiplas vozes e polifonia.

---

# 🎼 Estrutura Musical (Fuga)

Cada **linha do texto representa uma voz musical independente**.

As vozes são processadas simultaneamente, criando **polifonia**, característica típica das fugas de Bach.

Exemplo de texto:

```
[0] C D E F
[4] G A B C
```

Interpretação:

- Linha 1 → Voz 0 inicia imediatamente
- Linha 2 → Voz 1 inicia após **4 beats de atraso**

Isso cria entradas sucessivas das vozes, simulando uma **estrutura de fuga**.

---

# 🎹 Parâmetros Iniciais por Voz

Cada voz possui parâmetros iniciais diferentes para simular registros musicais distintos.

| Voz | Oitava Base | Volume | Instrumento |
|----|----|----|----|
| V0 | 6 | 100 | Cravo (GM 6) |
| V1 | 5 | 80 | Órgão (GM 20) |
| V2 | 4 | 60 | Piano (GM 0) |
| V3 | 3 | 40 | Fagote (GM 70) |

Após a voz 3, os valores **se repetem em ciclo**.

---

# 🎵 Mapeamento de Caracteres

## Notas Musicais

| Caractere | Nota |
|------|------|
| A | Lá |
| B | Si |
| C | Dó |
| D | Ré |
| E | Mi |
| Mb | Mi bemol |
| F | Fá |
| G | Sol |
| H | Si bemol |

## Pausas

Letras minúsculas representam pausas:

```
a b c d e f g h
```

---

# 🎛 Controles Musicais

| Símbolo | Função |
|------|------|
| `?` | aumenta uma oitava |
| `V` | diminui uma oitava |
| `>` | aumenta BPM em 10 |
| `<` | diminui BPM em 10 |
| `[n]` | atraso inicial da voz em beats |
| `!` | instrumento Harmonica (GM 22) |
| `;` | instrumento Tubular Bells (GM 15) |
| `,` | instrumento Church Organ (GM 20) |
| espaço | dobra o volume (até 127) |

Alterações de **volume e oitava são locais à voz**.

---

# ⏱ Controle de Tempo

O andamento inicial da música é:

```
BPM inicial = 120
```

Os caracteres especiais podem alterar o andamento:

```
> aumenta BPM
< diminui BPM
```

Essas alterações afetam **toda a peça musical**.

---

# 📂 Entrada de Dados

O texto pode ser inserido de três formas:

- digitado diretamente no sistema
- carregado de um arquivo `.txt`
- editado e salvo novamente no arquivo

Caso o arquivo seja modificado, o sistema deve permitir **salvar substituindo o original**.

---

# 📀 Saída do Sistema

O sistema deve gerar:

- reprodução sonora da música
- arquivo **MIDI**

O arquivo MIDI pode:

- ter nome padrão definido pelo sistema  
ou
- ter nome escolhido pelo usuário

Também pode ser salvo em:

- diretório padrão  
ou
- diretório escolhido pelo usuário

---

# ⚙️ Parâmetros Globais

```
BPM inicial: 120
Volume máximo: 127
Oitava mínima: 0
Oitava máxima: 9
```

---

# 🧠 Estrutura do Projeto

Sugestão de organização do projeto:

```
music-text-generator/
│
├── src/
│   ├── parser.py
│   ├── midi_generator.py
│   ├── voice.py
│   └── player.py
│
├── examples/
│   └── exemplo_fuga.txt
│
├── docs/
│   └── documentacao.pdf
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🚀 Como Executar o Projeto

Clone o repositório:

```bash
git clone https://github.com/seuusuario/music-text-generator.git
```

Entre na pasta do projeto:

```bash
cd music-text-generator
```

Execute o programa:

```bash
python main.py
```

---

# 🧪 Testes e Depuração

Antes da demonstração para o professor, o sistema deve ser:

- testado
- depurado
- validado com diferentes arquivos de texto

para garantir que o gerador de música funcione corretamente.

---

# 📋 Etapas do Trabalho (Fase 2)

## 1ª Parte
Atualizar a lista de **requisitos funcionais e não funcionais**, incluindo as novas funcionalidades desta fase.

## 2ª Parte
**Reprojetar a parte funcional do sistema**, adicionando novas classes ao projeto desenvolvido na Fase 1.

## 3ª Parte
**Reprojetar a interface com o usuário**, incluindo telas ou elementos necessários para suportar as novas funcionalidades.

Cada tela deve ser apresentada na documentação com:

- imagem da interface
- explicação do layout
- justificativa das escolhas de design.

## 4ª Parte
**Implementar o protótipo do sistema**, utilizando a tecnologia escolhida pelo grupo.

É permitido reutilizar código existente, desde que:

- seja informado na documentação
- seja justificado o motivo do uso.

O sistema deve ser **testado e depurado antes da apresentação**.

## 5ª Parte
Apresentar o projeto ao professor, demonstrando:

- funcionamento do sistema
- principais características
- implementação realizada

A documentação final e o código devem ser entregues até o dia da demonstração.

O professor poderá:

- analisar o repositório no **GitHub**
- fazer perguntas aos integrantes do grupo sobre o projeto.

Todos os membros devem demonstrar participação no desenvolvimento.

  
- https://pt.wikipedia.org/wiki/General_MIDI
