# Projeto IP 2025.2 - Equipe 3
Projeto da disciplina de Introdução à Programação 2025.2 (CC/IA) - UFPE
# 1. Título do projeto: 

  -1Gorila vs (CIN)Homens

# 2. Equipe e suas atribuições:
  -Allan Fernandes de Lucena afl4
    -Responsável por parte do código referente ao ataque especial, aos atributos, disparo , tela inicial e tela de gameover para iniciar e encerrar o jogo. Dos coletáveis, elaborou a parte do XP.
  
  -Gustavo Nascimento de Oliveira - gno -
    -Responsável pela gestão de tarefas, por alguns sprites utilizados no jogo e do relatório no github.
  
  -Kaio Vinicius Pereira Moura - kvpm -
    -Responsável pela elaboração dos slides e de alguns sprites utilizados no jogo.

  -Marcos Antônio de Oliveira Neto - maon -
    -Responsável por parte do código referente a camêra que segue o jogador, Spawn de inimigos, colisão. Dos coletáveis, elaborou a parte das bananas, das moedas e da pedra.
  
  -Matheus Miranda Borges dos Santos - mmbs2 -
    -Responsável pela elaboração do do mapa a partyir da ferramenta tiledmap e do relatório no github. 
  
# 3. Sobre o Jogo:
  3.1 História:
    - Um Gorila, filósofo, que incentiva seus seguidores com a sua frase mais inspiradora "Apenas comece" que vem dá filosofia mais refinada, estava a viver a sua vida em paz. Entretanto, ele é capturado por um grupo de calouros do CIN para enfrentar um desafio: Derrotar os (CIN)homens enquanto percorre um trajeto tortuoso em busca de amadurecimento(XP), alimento(banana), pedras e moedas, é claro!

  3.2 Personagens:
    -Gorila filósofo(personagem principal e jogável)
    -CIN(homens)-Adversários que tiram vida do personagem principal

  3.3 Mecânica do jogo:
    -O personagem principal(Gorila filósofo), se desloca pelo mapa coletando xp, bananas, moedas e pedra.

# 4. Estrutura e Organização do código
```text
📂 projeto
├── 📂 assets                # Recursos visuais e sonoros
│   ├── 📂 images
│   │   ├── 📂 player        # Sprites do jogador (left/right)
│   │   ├── 📂 enemy         # Sprites dos inimigos (left/right)
│   │   └── sprites gerais  # Coletáveis, UI e telas
│   └── 📂 sounds            # Trilha sonora do jogo
│
├── 📂 data                  # Dados do mundo do jogo
│   ├── 📂 graphics
│   │   ├── 📂 objects       # Objetos do cenário
│   │   └── 📂 tilesets      # Tilesets gráficos
│   ├── 📂 maps              # Mapas (.tmx)
│   └── 📂 tilesets          # Definições dos tiles (.tsx)
│
└── 📂 src                   # Código-fonte
    ├── main.py              # Ponto de entrada do jogo
    ├── player.py            # Lógica do jogador
    ├── enemies.py           # Lógica dos inimigos
    ├── coletaveis.py        # Sistema de coletáveis
    ├── collision.py         # Detecção de colisões
    ├── aim.py               # Sistema de mira
    ├── store.py             # Loja / atributos
    └── utilidades           # Sprites, entidades e botões
```

# 5. Capturas de tela:
<img width="946" height="633" alt="image" src="https://github.com/user-attachments/assets/c56d518b-ea17-4a0a-8f31-e568699fbbd3" />

<img width="945" height="631" alt="image" src="https://github.com/user-attachments/assets/a1b7e4ad-0677-49df-bdc8-e95c6a87c499" />

<img width="1917" height="985" alt="image" src="https://github.com/user-attachments/assets/116c2af5-202d-4c66-85ff-110391a16672" />

<img width="1065" height="826" alt="image" src="https://github.com/user-attachments/assets/c47ca993-61c6-4122-9f20-801141994b8b" />

<img width="1080" height="830" alt="image" src="https://github.com/user-attachments/assets/0ce09a62-fee4-4b18-a4bf-e1ba1084c881" />



# 6. Ferramentas, bibliotecas, frameworks:
  -Ferramentas utilizadas:
  
    -Pygame-ce(Biblioteca usada para o desenvolvimento de jogos 2D na linguagem Python - (Linguagem utilizda durante a cadeira de Introdução à Programação 2025.2 (CC/IA) - UFPE)

    -Vscode(Editor de código (utilisado para escrever, depurar e testar código em diversas linguagens-nesse projeto a linguagem de programação uitlizada foi Python), introduzido e utilizado durante a cadeira de Introdução à Programação 2025.2 (CC/IA) - UFPE)
    
    -Whatsapp(Comunicação mais dinâmica os membros do grupo responsáveis pela elaboração do projeto)
    
    -Discord(comunicação por áudio e texto utilizada para reuniões entre os membros do grupo e para discussões acerca de aspectos do projeto)
    
    -Email(Envio de arquivos, pastas)
    
    -Git(versionamneto de código local)
    
    -GitHub(Colaboração e compartilhamento de código no repositório)
    
    -Notion(Estruturação dos afazeres- das tarefas para a conclusão do projeto)
    
    -Tiled Map Editor(Ferramenta de elaboração de mapas)
    
    -Pixilart(Elaboração de alguns frames utilizados na elaboração do jogo)
    
    -Youtube(Aprendizados diversos relacionados a outras ferramentas para a elaboração do projeto)

# 7. Como jogar:

  -Movimento: 
    
    -Tecla Enter(inicia o jogo)
  
    -Tecla W(Move para cima)
    
    -Tecla A(Move para a esquerda)
    
    -Tecla S(Move para baixo)
    
    -Tecla D(Move para a Direita)
    
  -Disparo:

    -Botão esquerdo do Mouse(Disparo de projéteis-pedras)
    -Botão direito do Mouse(Dispara um ataque do tipo soco)
    
  -Outras teclas para o jogo:
  
    -Tecla H(para curar)

    -Tecla L(para abrir a loja)

    -Tecla M(para abrir o menu skills)

    -Tecla E(para usaro especial)
    
# 8. Os conceitos que foram apresentados durante a disciplina e utilizados no projeto (indicando onde foram usados):

  -Estruturas condicionais: Controlam a resposta dada caso uma condição seja verdadira. Exemplo: Caso o jogador acione a tecla W o personagem principal andará para cima.
  
  -Programação orientada a Objetos: Uma forma de elaboração do código do jogo, com classes, atributos e métodos.
  
  -Funções: Um agrupamento de um bloco de código que pode ser utilizado em diversas partes do código.
  
# 9. Desafios, erros e aprendizados:
  -Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?
  
    -Tempo escasso se revelou um problema que acometeu vários aspectos da realização do projeto, mas com afinco foi possível superar algumas dessas questões realcionadas ao tempo curto. Dentre esses aspectos, encontramos uma dificuldade na hora de importar o mapa, mas essa dificuldade foi contornada após alguns ciclos de tentativa e erro.
    
  -Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?
  
    -Aprendizado de novas ferramentas e conceitos (OOP) em pouco tempo. A gestão do tempo em meio a diversos compromissos e tarefas associados ao projeto,e outros compromissos não relacionados ao projeto, foi ,de fato, desafiador.

  -Quais as lições aprendidas durante o projeto?
  
    - O trabalho colaborativo, atrelado a uma comunicação dinâmica(por meio de aplicativos), foi essencial para a realização do projeto, apesar das dificuldades encontradas com o tempo escasso. Atrelado a isso, o uso de ferramentas como o GIT e GitHub nos proporcionaram uma visão do trabalho colaborativo em um projeto de multiplas contribuições. A importância do trabalho em equipe ficou evidente na elaboração do projeto, com os membros se colocando a disposição para auxiiar, uns aos outros, durante as atividades e as demandas, ou dificuldades, que foram surgindo ao longo do projeto. A importancia da gestão do tempo também se mostrou como algo essencial para uma boa realização de um projeto como esse.

  
