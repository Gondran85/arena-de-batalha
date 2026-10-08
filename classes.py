import random  # Usado para sortear acertos, erros, variação de dano e cura


# ==========================================================
# CONSTANTES DO JOGO
# ==========================================================

# Vida máxima que qualquer personagem pode ter
VIDA_MAXIMA = 100

# Chance (em %) de um ataque que acertou virar um golpe crítico
CHANCE_CRITICO = 12

# Multiplicador aplicado ao dano quando o golpe é crítico
MULTIPLICADOR_CRITICO = 1.5


# ==========================================================
# GOLPES DISPONÍVEIS
# ==========================================================

# Cada golpe tem um dano base e uma precisão (chance de acertar em %).
# Regra de equilíbrio: quanto mais forte o golpe, menor a precisão.
golpes = {
    "Soco":        {"dano": 8,  "precisao": 95},
    "Rasteira":    {"dano": 10, "precisao": 92},
    "Cotovelada":  {"dano": 12, "precisao": 90},
    "Uppercut":    {"dano": 14, "precisao": 85},
    "Gancho":      {"dano": 16, "precisao": 82},
    "Pontapé":     {"dano": 18, "precisao": 80},
    "Joelhada":    {"dano": 20, "precisao": 75},
    "Cabeçada":    {"dano": 22, "precisao": 70},
    "Voadora":     {"dano": 25, "precisao": 65},
    "Golpe Final": {"dano": 35, "precisao": 45},
}


# ==========================================================
# CLASSE PERSONAGEM
# ==========================================================

class Personagem:

    def __init__(self, nome, golpes, vida=VIDA_MAXIMA):
        self.nome = nome                  # Nome do personagem
        self.golpes = golpes              # Dicionário de golpes disponíveis
        self.vida_maxima = VIDA_MAXIMA    # Teto de vida do personagem
        self.vida = min(vida, VIDA_MAXIMA)  # Vida atual (nunca acima do teto)

    # ------------------------------------------------------
    # RECEBER DANO
    # ------------------------------------------------------

    def receber_dano(self, dano):
        self.vida -= dano    # Reduz a vida pelo dano recebido

        if self.vida < 0:    # Garante que a vida não fique negativa
            self.vida = 0

    # ------------------------------------------------------
    # ATACAR
    # ------------------------------------------------------

    def atacar(self, alvo, golpe):
        # Busca os dados do golpe escolhido
        dados = self.golpes[golpe]

        # Sorteia um número de 1 a 100 para testar a precisão do golpe
        sorte = random.randint(1, 100)

        # Se o sorteio for maior que a precisão, o golpe errou
        if sorte > dados["precisao"]:
            return {
                "golpe": golpe,
                "acertou": False,
                "critico": False,
                "dano": 0,
            }

        # O golpe acertou: aplica uma pequena variação no dano base
        dano = dados["dano"] + random.randint(-2, 2)

        # Agora sorteia se o acerto virou um golpe crítico
        critico = random.randint(1, 100) <= CHANCE_CRITICO

        if critico:
            dano = int(dano * MULTIPLICADOR_CRITICO)

        # O dano nunca pode ser menor que 1
        if dano < 1:
            dano = 1

        # Aplica o dano no alvo
        alvo.receber_dano(dano)

        return {
            "golpe": golpe,
            "acertou": True,
            "critico": critico,
            "dano": dano,
        }

    # ------------------------------------------------------
    # CURAR
    # ------------------------------------------------------

    def curar(self):
        # Sorteia quanto de cura o personagem recebeu
        cura = random.randint(10, 28)

        # Guarda a vida antes da cura para calcular o ganho real
        vida_antes = self.vida

        # Aplica a cura sem passar da vida máxima
        self.vida = min(self.vida + cura, self.vida_maxima)

        # Retorna apenas o que realmente foi curado
        return self.vida - vida_antes

    # ------------------------------------------------------
    # ESTÁ VIVO
    # ------------------------------------------------------

    def esta_vivo(self):
        return self.vida > 0    # True se ainda tem vida

    # ------------------------------------------------------
    # PERCENTUAL DE VIDA
    # ------------------------------------------------------

    def percentual_vida(self):
        return self.vida / self.vida_maxima    # Valor de 0.0 até 1.0
