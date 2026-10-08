# Arena de Batalha

Jogo de combate por turnos jogado no terminal, feito em Python com foco em
Programação Orientada a Objetos. Você enfrenta o computador escolhendo golpes
com dano e precisão diferentes até que um dos dois fique sem vida.

A interface é desenhada com a biblioteca [Rich](https://github.com/Textualize/rich):
painéis para cada lutador, barras de vida coloridas, tabela de golpes e um
histórico do combate que se atualiza a cada turno.

## Como funciona

- Cada lutador começa com **100 pontos de vida**.
- São **10 golpes** disponíveis, de `Soco` (8 de dano, 95% de precisão) até
  `Golpe Final` (35 de dano, 45% de precisão).
- Regra de equilíbrio: **quanto mais forte o golpe, menor a chance de acertar**.
- Todo acerto tem **12% de chance de ser crítico**, multiplicando o dano por 1.5.
- O dano base varia de -2 a +2 a cada ataque, então o resultado nunca é fixo.
- Em vez de atacar, você pode **se curar** e recuperar de 10 a 28 de vida
  (sem passar do limite de 100).
- Quem começa a batalha é decidido por sorteio.

O computador decide sozinho o que fazer: com a vida acima de 35% ele prefere
atacar (80% das vezes), e abaixo disso passa a priorizar a cura (60% das vezes).

## Instalação

Requer Python 3.10 ou superior.

```bash
pip install -r requirements.txt
```

## Como jogar

```bash
python main.py
```

Digite o nome do seu personagem e, a cada turno, escolha entre atacar (`1`) ou
curar (`2`). Ao atacar, a tabela mostra o dano e a precisão de cada golpe para
você decidir se vale arriscar.

## Estrutura

| Arquivo | Responsabilidade |
| --- | --- |
| `classes.py` | Regras do jogo: constantes, dicionário de golpes e a classe `Personagem` (atacar, receber dano, curar, checar vida). |
| `main.py` | Interface e fluxo da partida: telas, barras de vida, turnos do jogador e do computador, tela final. |

A separação é intencional: `classes.py` não imprime nada na tela e `main.py`
não contém regras de combate.

## Conceitos de POO aplicados

- **Classe e objetos**: `Personagem` é instanciada duas vezes (jogador e computador).
- **Encapsulamento**: a vida só muda através dos métodos `receber_dano` e `curar`,
  que garantem os limites de 0 e 100.
- **Métodos de estado**: `esta_vivo` e `percentual_vida` expõem a situação do
  personagem sem deixar o código externo mexer nos atributos direto.
- **Reuso**: o mesmo código de ataque serve para o jogador e para a CPU.

## Sobre

Desafio 027 dos meus estudos de Python e Programação Orientada a Objetos.
