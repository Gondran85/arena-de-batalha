from classes import Personagem   # Importa a classe Personagem
from classes import golpes       # Importa o dicionário de golpes
from classes import VIDA_MAXIMA  # Importa o limite de vida do jogo

import random  # Usado para decisões aleatórias do computador

from rich.console import Console  # Exibe mensagens estilizadas no terminal
from rich.panel import Panel      # Cria painéis estilizados
from rich.table import Table      # Cria tabelas estilizadas
from rich.text import Text        # Monta textos coloridos (barras de vida)
from rich.align import Align      # Centraliza conteúdo dentro dos painéis


# Cria o objeto Console para exibir informações com Rich
console = Console()

# Quantidade de blocos usados para desenhar a barra de vida
LARGURA_BARRA = 22

# Quantas linhas do histórico de combate ficam visíveis na tela
LINHAS_REGISTRO = 7


# ==========================================================
# FUNÇÃO: COR DA VIDA
# ==========================================================

def cor_vida(personagem):
    # Calcula o percentual de vida restante
    percentual = personagem.percentual_vida()

    # Vida alta fica verde, média amarela e baixa vermelha
    if percentual > 0.6:
        return "green"

    if percentual > 0.3:
        return "yellow"

    return "red"


# ==========================================================
# FUNÇÃO: BARRA DE VIDA
# ==========================================================

def barra_vida(personagem):
    # Descobre quantos blocos devem ficar preenchidos
    cheios = int(personagem.percentual_vida() * LARGURA_BARRA)

    # O resto da barra fica vazio
    vazios = LARGURA_BARRA - cheios

    # Monta o texto da barra em duas partes coloridas
    barra = Text()
    barra.append("█" * cheios, style=cor_vida(personagem))
    barra.append("░" * vazios, style="grey37")

    # Acrescenta o número de pontos de vida no final
    barra.append(
        f"  {personagem.vida:>3}/{personagem.vida_maxima}",
        style=f"bold {cor_vida(personagem)}"
    )

    return barra


# ==========================================================
# FUNÇÃO: PAINEL DE UM LUTADOR
# ==========================================================

def painel_lutador(personagem, icone, cor):
    # Junta o ícone e o nome em uma linha só
    conteudo = Text()
    conteudo.append(f"{icone}  {personagem.nome}\n\n", style=f"bold {cor}")

    # Adiciona a barra de vida embaixo do nome
    conteudo.append_text(barra_vida(personagem))

    return Panel(
        conteudo,
        border_style=cor,
        padding=(1, 2)
    )


# ==========================================================
# FUNÇÃO: DESENHAR A TELA DA BATALHA
# ==========================================================

def desenhar_tela(jogador, computador, registro, turno):
    # Limpa o terminal para a tela ficar sempre organizada
    console.clear()

    # Título da arena
    console.print(
        Panel(
            Align.center("[bold yellow]A R E N A   D E   B A T A L H A[/]"),
            border_style="bright_yellow"
        )
    )

    # Tabela invisível usada só para colocar os dois painéis lado a lado
    placar = Table.grid(expand=True)
    placar.add_column(ratio=1)
    placar.add_column(ratio=1)

    placar.add_row(
        painel_lutador(jogador, "[*]", "cyan"),
        painel_lutador(computador, "[CPU]", "magenta")
    )

    console.print(placar)

    # Monta o histórico das últimas ações da batalha
    historico = Text()

    # Pega apenas as últimas linhas do registro
    ultimas = registro[-LINHAS_REGISTRO:]

    if ultimas:
        for linha in ultimas:
            historico.append_text(Text.from_markup(linha))
            historico.append("\n")

    else:
        historico.append_text(
            Text.from_markup("[grey62]A batalha está começando...[/]")
        )

    console.print(
        Panel(
            historico,
            title=f"[bold]Combate - Turno {turno}[/]",
            border_style="grey50",
            padding=(1, 2)
        )
    )


# ==========================================================
# FUNÇÃO: MOSTRAR GOLPES
# ==========================================================

def mostrar_golpes(personagem):
    # Cria uma tabela para mostrar os golpes disponíveis
    tabela = Table(
        title="[bold yellow]Golpes disponíveis[/]",
        header_style="bold white",
        border_style="yellow"
    )

    # Cria as colunas da tabela
    tabela.add_column("N", justify="center", style="bold cyan")
    tabela.add_column("Golpe", style="bold")
    tabela.add_column("Dano", justify="center", style="red")
    tabela.add_column("Precisão", justify="center")
    tabela.add_column("Confiança", justify="left")

    # Percorre todos os golpes do personagem
    for numero, (golpe, dados) in enumerate(personagem.golpes.items(), start=1):
        precisao = dados["precisao"]

        # A cor da precisão mostra o quanto o golpe é confiável
        if precisao >= 85:
            cor = "green"

        elif precisao >= 70:
            cor = "yellow"

        else:
            cor = "red"

        # Desenha uma mini barra para representar a precisão visualmente
        cheios = round(precisao / 10)
        confianca = f"[{cor}]{'=' * cheios}[/][grey37]{'-' * (10 - cheios)}[/]"

        tabela.add_row(
            str(numero),
            golpe,
            str(dados["dano"]),
            f"[{cor}]{precisao}%[/]",
            confianca
        )

    # Exibe a tabela
    console.print(tabela)


# ==========================================================
# FUNÇÃO: ESCOLHER GOLPE
# ==========================================================

def escolher_golpe(jogador):
    # Cria uma lista contendo apenas os nomes dos golpes
    lista_golpes = list(jogador.golpes.keys())

    # Mostra os golpes antes da escolha
    mostrar_golpes(jogador)

    while True:
        # Recebe a escolha do usuário
        escolha_golpe = console.input(
            "[bold yellow]> Escolha o número do golpe: [/]"
        )

        # Verifica se o usuário digitou apenas números
        if escolha_golpe.isdigit():
            escolha_golpe = int(escolha_golpe)

            # Verifica se o número escolhido existe na lista
            if 1 <= escolha_golpe <= len(lista_golpes):
                golpe_escolhido = lista_golpes[escolha_golpe - 1]

                # Retorna o nome do golpe escolhido
                return golpe_escolhido

        # Caso a escolha seja inválida, repete o while
        console.print("[bold red]Golpe inválido. Tente novamente.[/]")


# ==========================================================
# FUNÇÃO: DESCREVER O ATAQUE
# ==========================================================

def descrever_ataque(atacante, alvo, resultado, cor):
    # O golpe errou o alvo
    if not resultado["acertou"]:
        return (
            f"[{cor}]{atacante.nome}[/] tentou "
            f"[bold yellow]{resultado['golpe']}[/] e "
            f"[bold grey62]errou o golpe![/]"
        )

    # O golpe acertou como crítico
    if resultado["critico"]:
        return (
            f"[{cor}]{atacante.nome}[/] acertou um "
            f"[bold red]{resultado['golpe']} CRITICO[/] "
            f"causando [bold red]{resultado['dano']}[/] de dano "
            f"em {alvo.nome}!"
        )

    # O golpe acertou normalmente
    return (
        f"[{cor}]{atacante.nome}[/] acertou "
        f"[bold yellow]{resultado['golpe']}[/] "
        f"causando [bold red]{resultado['dano']}[/] de dano "
        f"em {alvo.nome}."
    )


# ==========================================================
# FUNÇÃO: TURNO DO JOGADOR
# ==========================================================

def turno_jogador(jogador, computador, registro, turno):

    while True:
        # Redesenha a tela a cada tentativa de escolha
        desenhar_tela(jogador, computador, registro, turno)

        console.print("\n[bold cyan]Sua vez, escolha uma ação:[/]")
        console.print("  [bold]1[/] - Atacar")
        console.print("  [bold]2[/] - Curar")

        escolha = console.input("\n[bold cyan]> Ação: [/]")

        # --------------------------------------------------
        # OPÇÃO 1: ATACAR
        # --------------------------------------------------

        if escolha == "1":
            # Descobre qual golpe o jogador escolheu
            golpe_escolhido = escolher_golpe(jogador)

            # Executa o ataque contra o computador
            resultado = jogador.atacar(computador, golpe_escolhido)

            # Guarda o resultado no histórico da batalha
            registro.append(
                descrever_ataque(jogador, computador, resultado, "bold cyan")
            )

            # Encerra o turno do jogador
            break

        # --------------------------------------------------
        # OPÇÃO 2: CURAR
        # --------------------------------------------------

        elif escolha == "2":
            # O método curar já aumenta a vida e retorna o valor da cura
            cura = jogador.curar()

            # Quando a vida já está cheia, a cura é desperdiçada
            if cura == 0:
                registro.append(
                    f"[bold cyan]{jogador.nome}[/] tentou se curar, mas a "
                    f"vida já estava [bold green]cheia[/]."
                )

            else:
                registro.append(
                    f"[bold cyan]{jogador.nome}[/] se curou e recuperou "
                    f"[bold green]{cura}[/] de vida."
                )

            # Encerra o turno do jogador
            break

        # --------------------------------------------------
        # OPÇÃO INVÁLIDA
        # --------------------------------------------------

        else:
            console.print("[bold red]Opção inválida. Escolha 1 ou 2.[/]")
            console.input("[grey62]Pressione Enter para continuar...[/]")


# ==========================================================
# FUNÇÃO: TURNO DO COMPUTADOR
# ==========================================================

def turno_computador(computador, jogador, registro, turno):

    # Mostra a tela atualizada antes da jogada do computador
    desenhar_tela(jogador, computador, registro, turno)

    console.print("\n[bold magenta]O computador está pensando...[/]")

    # O computador prefere se curar quando está com pouca vida
    if computador.percentual_vida() < 0.35:
        acao = random.choices(["atacar", "curar"], weights=[40, 60])[0]

    else:
        acao = random.choices(["atacar", "curar"], weights=[80, 20])[0]

    # ------------------------------------------------------
    # COMPUTADOR ESCOLHEU ATACAR
    # ------------------------------------------------------

    if acao == "atacar":
        # Cria uma lista com os nomes dos golpes
        lista_golpes = list(computador.golpes.keys())

        # Escolhe um golpe aleatoriamente
        golpe = random.choice(lista_golpes)

        # Executa o ataque contra o jogador
        resultado = computador.atacar(jogador, golpe)

        # Guarda o resultado no histórico da batalha
        registro.append(
            descrever_ataque(computador, jogador, resultado, "bold magenta")
        )

    # ------------------------------------------------------
    # COMPUTADOR ESCOLHEU CURAR
    # ------------------------------------------------------

    else:
        # Executa a cura
        cura = computador.curar()

        if cura == 0:
            registro.append(
                f"[bold magenta]{computador.nome}[/] tentou se curar, mas a "
                f"vida já estava [bold green]cheia[/]."
            )

        else:
            registro.append(
                f"[bold magenta]{computador.nome}[/] se curou e recuperou "
                f"[bold green]{cura}[/] de vida."
            )

    # Mostra a tela já com o resultado e espera o jogador ler
    desenhar_tela(jogador, computador, registro, turno)
    console.input("\n[grey62]Pressione Enter para continuar...[/]")


# ==========================================================
# FUNÇÃO: TELA FINAL
# ==========================================================

def tela_final(jogador, computador, registro, turno):
    # Mostra o estado final da arena
    desenhar_tela(jogador, computador, registro, turno)

    # Define quem ganhou e com qual estilo mostrar o resultado
    if jogador.esta_vivo():
        mensagem = f"[bold green]{jogador.nome} venceu a batalha![/]"
        detalhe = f"Vida restante: [bold green]{jogador.vida}/{VIDA_MAXIMA}[/]"
        cor = "green"

    else:
        mensagem = f"[bold red]{computador.nome} venceu a batalha![/]"
        detalhe = f"Vida restante: [bold red]{computador.vida}/{VIDA_MAXIMA}[/]"
        cor = "red"

    console.print(
        Panel(
            Text.from_markup(
                f"{mensagem}\n\n{detalhe}\n"
                f"[grey62]Turnos disputados: {turno}[/]",
                justify="center"
            ),
            title="[bold]FIM DA BATALHA[/]",
            border_style=cor,
            padding=(1, 4)
        )
    )


# ==========================================================
# FUNÇÃO PRINCIPAL
# ==========================================================

def main():

    # ------------------------------------------------------
    # TELA DE ABERTURA
    # ------------------------------------------------------

    console.clear()

    console.print(
        Panel(
            Text.from_markup(
                "[bold yellow]A R E N A   D E   B A T A L H A[/]\n\n"
                f"[grey62]Vida máxima: {VIDA_MAXIMA} - "
                f"Golpes disponíveis: {len(golpes)}\n"
                "Golpes fortes acertam menos. Escolha com estratégia![/]",
                justify="center"
            ),
            border_style="bright_yellow",
            padding=(1, 4)
        )
    )

    # ------------------------------------------------------
    # CRIAÇÃO DOS PERSONAGENS
    # ------------------------------------------------------

    nome_jogador = console.input(
        "\n[bold cyan]> Digite o nome do seu personagem: [/]"
    )

    # Usa um nome padrão caso o jogador não digite nada
    if not nome_jogador.strip():
        nome_jogador = "Jogador"

    # Cria o objeto do jogador
    jogador = Personagem(
        nome_jogador.strip(),
        golpes
    )

    # Cria o objeto do computador
    computador = Personagem(
        "Computador",
        golpes
    )

    # ------------------------------------------------------
    # SORTEIO DE QUEM COMEÇA
    # ------------------------------------------------------

    primeiro = random.choice([jogador, computador])

    # Lista que guarda tudo o que acontece na batalha
    registro = []

    registro.append(
        f"[bold yellow]O sorteio decidiu:[/] "
        f"[bold]{primeiro.nome}[/] começa a batalha!"
    )

    # Contador de turnos da batalha
    turno = 1

    # ------------------------------------------------------
    # LOOP PRINCIPAL DA BATALHA
    # ------------------------------------------------------

    while jogador.esta_vivo() and computador.esta_vivo():

        # ==================================================
        # JOGADOR COMEÇA
        # ==================================================

        if primeiro == jogador:

            turno_jogador(jogador, computador, registro, turno)

            # O computador só joga se ainda estiver vivo
            if computador.esta_vivo():
                turno_computador(computador, jogador, registro, turno)

        # ==================================================
        # COMPUTADOR COMEÇA
        # ==================================================

        else:

            turno_computador(computador, jogador, registro, turno)

            # O jogador só joga se ainda estiver vivo
            if jogador.esta_vivo():
                turno_jogador(jogador, computador, registro, turno)

        # Passa para o próximo turno
        turno += 1

    # ------------------------------------------------------
    # FINAL DA BATALHA
    # ------------------------------------------------------

    tela_final(jogador, computador, registro, turno - 1)


# ==========================================================
# PONTO DE ENTRADA DO PROGRAMA
# ==========================================================

if __name__ == "__main__":
    main()
