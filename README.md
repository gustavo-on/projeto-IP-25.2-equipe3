# 🦍 Um Gorila VS (CIn)Homens

Relatório de desenvolvimento do jogo **Um Gorila VS (CIn)Homens**, desenvolvido para a disciplina de **Introdução à Programação** do curso de **Ciência da Computação** – **UFPE / Centro de Informática (CIn)**, semestre **2025.2**, **Equipe 3**.

---

## 📑 Índice
- [1. Equipe](#equipe)
  - [1.1 Membros](#membros)
  - [1.2 Divisão de Tarefas](#divisao)
- [2. Principais Objetivos](#objetivos)
- [3. Sobre o Jogo](#sobre)
- [4. Como Instalar e Rodar o Jogo](#instalacao)
- [5. Controles](#controles)
- [6. Itens, Objetos e Recursos do Jogo](#itens)
- [7. Estrutura / Arquitetura do Projeto](#estrutura)
- [8. Ferramentas, Bibliotecas e Frameworks Utilizados](#ferramentas)
- [9. Conceitos da Disciplina Aplicados](#conceitos)
- [10. Desafios, Erros e Aprendizados](#desafios)
- [11. Galeria / Capturas de Tela](#galeria)

---

<a id="equipe"></a>
## 👥 1. Equipe

<a id="membros"></a>
### 1.1 Membros

<div align="center">
<table width="100%">
<tr>
<td align="center">
<a href="https://github.com/AllanF-0101">
<img src="https://avatars.githubusercontent.com/u/244098995?v=4" width="100px"><br/>
<sub><b>Allan Fernandes de Lucena</b></sub>
</a><br/>
<sub>afl4</sub>
</td>

<td align="center">
<a href="https://github.com/gustavo-on">
<img src="https://avatars.githubusercontent.com/u/248238638?v=4" width="100px"><br/>
<sub><b>Gustavo Nascimento de Oliveira</b></sub>
</a><br/>
<sub>gno</sub>
</td>

<td align="center">
<a href="https://github.com/kaio-mp3">
<img src="https://avatars.githubusercontent.com/u/248941971?v=4" width="100px"><br/>
<sub><b>Kaio Vinicius Pereira Moura</b></sub>
</a><br/>
<sub>kvpm</sub>
</td>

<td align="center">
<a href="https://github.com/marctnis">
<img src="https://avatars.githubusercontent.com/u/131407312?v=4" width="100px"><br/>
<sub><b>Marcos Antônio de Oliveira Neto</b></sub>
</a><br/>
<sub>maon</sub>
</td>

<td align="center">
<a href="https://github.com/Matheus-MB1">
<img src="https://avatars.githubusercontent.com/u/240080750?v=4" width="100px"><br/>
<sub><b>Matheus Miranda Borges dos Santos</b></sub>
</a><br/>
<sub>mmbs2</sub>
</td>
</tr>
</table>
</div>

---

<a id="divisao"></a>
### 📋 1.2 Divisão de Tarefas

- **Allan Fernandes de Lucena <afl4>:** Responsável por parte do código referente ao ataque especial, aos atributos, disparo , tela inicial e tela de gameover para iniciar e encerrar o jogo, música do jogo. Dos coletáveis, elaborou o sistema de XP.
- **Gustavo Nascimento de Oliveira <gno>:** Responsável pela gestão de tarefas, por sprites utilizados no jogo, design, criação do repositório no github, e do relatório no github.
- **Kaio Vinicius Pereira Moura <kvpm>:** Responsável pela elaboração dos slides, sprites de personagens utilizados no jogo e desing visual do jogo.
- **Marcos Antônio de Oliveira Neto <maon>:** Responsável por parte do código referente a camêra que segue o jogador, Spawn de inimigos, o sistema de colisões. Dos coletáveis, elaborou a parte das bananas, das moedas e da pedra.
- **Matheus Miranda Borges dos Santos <mmbs2>:** Responsável pela elaboração do do mapa a partir da ferramenta tiledmap e do relatório no github.

---

<a id="objetivos"></a>
## 🎯 2. Principais Objetivos

- Integrar os conhecimentos trabalhados em sala de aula por meio do desenvolvimento de um jogo 2D interativo.
- Aplicar lógica de programação e Programação Orientada a Objetos utilizando Python.
- Implementar um sistema de coleta com múltiplos tipos de itens e controle de pontuação.
- Desenvolver mecânicas de progressão por experiência e inimigos organizados em ondas com níveis de dificuldade.
- Estruturar o projeto de forma organizada, respeitando os requisitos mínimos da disciplina.

---

<a id="sobre"></a>
## 🎮 3. Sobre o Jogo

**Um Gorila VS CIn Homens** é um **twin-stick shooter 2D**, com câmera **top-down**, no qual o jogador controla um gorila em um mapa amplo, enfrentando ondas de inimigos humanos enquanto coleta recursos para sobreviver e evoluir.

### 📜 História
Um gorila filósofo, conhecido por inspirar seus seguidores com a frase **“Apenas comece”**, vivia sua vida em paz, guiado por uma filosofia simples e refinada.
Entretanto, ele é capturado por um grupo de calouros do **CIn**, sendo forçado a enfrentar um desafio: derrotar os **(CIn)Homens** enquanto percorre um trajeto tortuoso em busca de amadurecimento (**XP**), alimento (**bananas**), **pedras** e **moedas**.

### 👾 Personagens
- **Gorila Filósofo** – Personagem principal e jogável.
- **CIn Homens** – Inimigos que causam dano ao jogador.

### ⚙️ Mecânicas de Jogo
- Movimento livre em mapa top-down.
- Combate corpo a corpo e à distância.
- Coleta de XP, moedas, bananas e pedras.
- Evolução de atributos ao subir de nível.

---

<a id="instalacao"></a>
## 🚀 4. Como Instalar e Rodar o Jogo

### 1. Clone o repositório
```bash
git clone [https://github.com/gustavo-on/projeto-IP-25.2-equipe3.git](https://github.com/gustavo-on/projeto-IP-25.2-equipe3.git)
cd projeto-IP-25.2-equipe3
```
### 2. Instale as dependências
```bash
pip install -r requirements.txt
```
### 3. Execute o jogo
```bash
python src/main.py
```

<a id='controles'></a>
## 5. Controles

| Ação | Tecla / Entrada |
|------|----------------|
| Iniciar o jogo | Enter |
| Movimento | W, A, S, D |
| Mirar | Mouse |
| Soco | Clique esquerdo |
| Atirar pedra | Clique direito |
| Reiniciar (após morte) | R |
| Usar banana (cura) | H |
| Ataque especial | E |
| Abrir / fechar loja | L |
| Abrir / fechar menu | M |

---

<a id="itens"></a>
## 🎒 6. Itens, Objetos e Recursos do Jogo

| Item / Recurso | Sprite | Descrição e Utilidade |
| :---: | :---: | :--- |
| **Moeda** | <img src="https://github.com/gustavo-on/projeto-IP-25.2-equipe3/blob/main/assets/images/moeda.png?raw=true" width="50px"> | Utilizada para compras na loja. A cada **4 moedas**, o jogador pode adquirir uma banana ou uma pedra. |
| **Pedra** | <img src="https://github.com/gustavo-on/projeto-IP-25.2-equipe3/blob/main/assets/images/pedra.png?raw=true" width="50px"> | Item utilizado como munição para ataques à distância. É um recurso limitado, mas reaparece no mapa em determinados momentos. |
| **Banana** | <img src="https://github.com/gustavo-on/projeto-IP-25.2-equipe3/blob/main/assets/images/banana.png?raw=true" width="50px"> | Item de cura que recupera **3 pontos de vida** do personagem. |
| **XP** |  | Coletado por colisão. Ao subir de nível, permite escolher: Aumento de dano, vida máxima ou velocidade de movimento. |

---

<a id="estrutura"></a>
## 7. Estrutura / Arquitetura do Projeto

```text
📂 projeto
├── 📂 assets
│   ├── 📂 images
│   │   ├── 📂 enemy
│   │   │   ├── frames_left
│   │   │   └── frames_right
│   │   └── 📂 player
│   │       ├── frames_left
│   │       └── frames_right
│   │
│   │   TelaInicial.jpeg
│   │   TelaGameOver.jpg
│   │   attribute_menu.png
│   │   banana.png
│   │   cortebaixo.png
│   │   cortecima.png
│   │   cortedireita.png
│   │   corteesquerda.png
│   │   mira.png
│   │   moeda.png
│   │   pedra.png
│   │   punch.png
│   └── 📂 sounds
│       └── MusicaJogo.mp3
│
├── 📂 data
│   ├── 📂 graphics
│   │   ├── 📂 objects
│   │   └── 📂 tilesets
│   ├── 📂 maps
│   │   ├── aaworld.tmx
│   │   └── world.tmx
│   └── 📂 tilesets
│       ├── Objects.tsx
│       └── world_tileset.tsx
│
├── 📂 src
│   ├── aim.py
│   ├── allsprites.py
│   ├── button.py
│   ├── coletaveis.py
│   ├── collision.py
│   ├── enemies.py
│   ├── entity.py
│   ├── main.py
│   ├── player.py
│   ├── sprite.py
│   └── store.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

<a id="ferramentas"></a>
## 🛠️ 8. Ferramentas, Bibliotecas e Frameworks Utilizados

- **Python**: Linguagem de programação utilizada no desenvolvimento do jogo.
- **Pygame-CE**: Biblioteca principal para desenvolvimento 2D, renderização, eventos e áudio.
- **PyTMX**: Leitura e interpretação dos mapas criados no Tiled.
- **Visual Studio Code (VS Code)**: Editor de código para escrita e depuração.
- **Git & GitHub**: Versionamento de código e colaboração.
- **Tiled Map Editor**: Criação e edição dos mapas do jogo.
- **Pixilart**: Criação de sprites e frames gráficos.
- **YouTube**: Fonte de aprendizado complementar.

---

<a id="conceitos"></a>
## 🧠 9. Conceitos da Disciplina Aplicados

### 🔹 Estruturas Condicionais
Utilizadas para controlar o comportamento do jogo a partir de decisões lógicas.
Exemplo: ao pressionar a tecla **W**, o personagem principal se move para cima.

### 🔹 Programação Orientada a Objetos
O projeto foi estruturado com base em Programação Orientada a Objetos, utilizando classes, atributos e métodos para representar entidades como jogador, inimigos e itens coletáveis.

### 🔹 Funções
Utilização de funções para agrupar blocos de código reutilizáveis, facilitando a organização, manutenção e legibilidade do código.

---

<a id="desafios"></a>
## 🚧 10. Desafios, Erros e Aprendizados

### ❌ Maior Erro
Tempo escasso se revelou um problema que acometeu vários aspectos da realização do projeto, mas com afinco foi possível superar algumas dessas questões realcionadas ao tempo curto. Dentre esses aspectos, encontramos uma dificuldade na hora de importar o mapa, mas essa dificuldade foi contornada após alguns ciclos de tentativa e erro.

### 🔥 Maior Desafio
-Aprendizado de novas ferramentas e conceitos (OOP) em pouco tempo. A gestão do tempo em meio a diversos compromissos e tarefas associados ao projeto,e outros compromissos não relacionados ao projeto, foi ,de fato, desafiador.

### ✅ Lições Aprendidas
O trabalho colaborativo, atrelado a uma comunicação dinâmica(por meio de aplicativos), foi essencial para a realização do projeto, apesar das dificuldades encontradas com o tempo escasso. Atrelado a isso, o uso de ferramentas como o GIT e GitHub nos proporcionaram uma visão do trabalho colaborativo em um projeto de multiplas contribuições. A importância do trabalho em equipe ficou evidente na elaboração do projeto, com os membros se colocando a disposição para auxiiar, uns aos outros, durante as atividades e as demandas, ou dificuldades, que foram surgindo ao longo do projeto. A importancia da gestão do tempo também se mostrou como algo essencial para uma boa realização de um projeto como esse.

---

<a id="galeria"></a>
## 📸 11. Galeria / Capturas de Tela

<div align="center">
<table width="100%">
  <tr>
    <td width="50%">
      <img src="https://github.com/gustavo-on/projeto-IP-25.2-equipe3/blob/main/assets/images/Tela%20Inicial.jpeg?raw=true" alt="Print 1" width="100%">
      <br><sub>Tela de Início</sub>
    </td>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/c56d518b-ea17-4a0a-8f31-e568699fbbd3" alt="Print 2" width="100%">
      <br><sub>Legenda do Print 2</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/a1b7e4ad-0677-49df-bdc8-e95c6a87c499" alt="Print 3" width="100%">
      <br><sub>Legenda do Print 3</sub>
    </td>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/c47ca993-61c6-4122-9f20-801141994b8b" alt="Print 4" width="100%">
      <br><sub>Legenda do Print 4</sub>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <img src="https://github.com/user-attachments/assets/0ce09a62-fee4-4b18-a4bf-e1ba1084c881" alt="Print 5" width="100%">
      <br><sub>Legenda do Print 5</sub>
    </td>
    <td width="50%">
      <img src="URL_DO_PRINT_6" alt="Print 6" width="100%">
      <br><sub>Legenda do Print 6</sub>
    </td>
  </tr>
</table>
</div>
