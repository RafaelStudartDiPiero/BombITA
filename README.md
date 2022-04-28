# BombITA

O objetivo desse projeto é criar o jogo BombITA, baseado no jogo Bomberman da publicadora Konami.  
Em BombITA, cada jogador controla um personagem, com os personagems podendo se movimentar e soltar bombas. Os personagems estão dispostos em uma mapa retangular, onde 
existem paredes fixas, blocos, que são posicionados aleatoriamente no mapa, e um inimigo, que representa uma ameaça ao jogador, pois o personagem é eliminado
se entrar em contato com ele, fazendo com que o jogador perca o jogo e precise reiniciar.
A mecânica principal do jogo é a utilização das bombas, que podem destruir blocos, possibilitando novos caminhos de movimentação, o inimigo e jogadores, sendo necessário 
um cuidado para não se eliminar acidentalmente.  
Além disso, ao destruir blocos, existe a chance de ser gerado um _power_up_ que aumenta a velocidade do player.

# Arquitetura

Nosso projeto se baseiou no paradigma da Programação Orientada a Objetos, assim dividiu-se os componentes do jogo em classes, definindo as relações entre elas. Em seguida, uma breve explicação das classes:

## Game:  
  Representa uma instância do jogo e é formado por diferentes estados, alterando entre eles com base nos acontecimentos do jogo e decisões do jogador. Nessa classe, são definidos os métodos que alteram os modos de jogo e os eventos em cada modo.  
  
## Block:  
  Representa um bloco destrutível, definindo suas propriedades, como posição e chance de existir um powerup, e seu método para ser destruído pela bomba.  
  
## Bomb:  
  Representa uma bomba, pertecendo a um Player específico, definindo seus atributos, como sprites, estado atual e tempo de explosão, e seus métodos para interagir com os objetos externos.
  
## Enemy:  
  Representa um inimigo, determinando seus métodos para movimentação, interação com os Players e com a Bomba.
  
## Player:  
  Representa um personagem, caracterizando seus métodos para interagir com o inimigo, movimentar, considerando os blocos e paredes, soltar bombas e outras interações relevantes.
  
## PowerUp:  
  Representa uma classe Abstrata para ser herdada por outros powerups, facilitando a implementação deles.
  
## SpeedPowerUp:  
  Representa um powerup de velocidade, especificando a sua existência e seus efeitos.
  
# Conteúdo do Arquivos  


# Agradecimentos

Para o desenvolvimento do jogo, utilizou-se imagens fornecidas gratuitamente pelo site:  

https://www.spriters-resource.com  

E as músicas foram retiradas de:  

https://freemusicarchive.org/music/BoxCat_Games  
