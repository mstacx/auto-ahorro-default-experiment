from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Page,
)

import random

doc = """
Experimento: Auto-ahorro por default en billeteras digitales

Diseño:
- 12 rondas
- Ingreso aleatorio por ronda (80–120)
- Tratamiento: ahorro automático del 10%
- Shock financiero en ronda 8
- Los participantes deciden consumo y ahorro manual

Objetivo:
Evaluar si los defaults de ahorro influyen en el comportamiento
de ahorro bajo incertidumbre y shocks de liquidez.
"""


# CONSTANTES DEL EXPERIMENTO
class C(BaseConstants):
    NAME_IN_URL = "auto_ahorro_default"

    # No hay grupos (experimento individual)
    PLAYERS_PER_GROUP = None

    NUM_ROUNDS = 12

    DEFAULT_RATE = 0.1
    DEFAULT_RATE_PERCENT = 10

    SHOCK_ROUND = 8
    SHOCK_AMOUNT = 100

    MAX_INCOME = 120
    MIN_INCOME = 80


class Subsession(BaseSubsession):

    # Ingreso que recibirán todos los jugadores en esa ronda
    # Aleatorio [MIN_INCOME, MAX_INCOME] e igual para todos
    round_income = models.IntegerField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # ── Tratamiento
    # 0 = control (sin auto-ahorro)
    # 1 = tratamiento (auto-ahorro)
    treatment = models.IntegerField()

    # ── Variables sociodemograficas
    age = models.IntegerField(label="¿Cuántos años tienes?", min=14, max=80)
    gender = models.StringField(
        label="¿Cuál es tu género?",
        choices=[
            ["masculino", "Masculino"],
            ["femenino", "Femenino"],
        ],
        widget=widgets.RadioSelect,
    )
    university = models.StringField(
        label="¿En qué universidad estudias?",
        choices=[
            ["pucp", "PUCP"],
            ["up", "UP"],
            ["upc", "UPC"],
            ["unmsm", "UNMSM"],
            ["udep", "UDEP"],
            ["ucsur", "UCSUR"],
            ["uarm", "UARM"],
            ["unsa", "UNSA"],
            ["unsaac", "UNSAAC"],
            ["uadec", "UAdeC"],
        ],
        widget=widgets.RadioSelect,
    )
    career = models.StringField(
        label="¿Cuál es tu carrera universitaria?",
        choices=[
            ["economia", "Economía"],
            ["negocios", "Administración / Negocios / Finanzas / Contabilidad"],
            ["ingenieria", "Ingeniería / Computación"],
            [
                "ciencias_sociales",
                "Ciencias Sociales (Sociología, Sicología, Ciencia Política, etc.)",
            ],
            ["derecho", "Derecho"],
            ["salud", "Ciencias de la Salud (Medicina, Enfermería, etc.)"],
            [
                "ciencias_naturales",
                "Ciencias Naturales (Biología, Física, Química, etc.)",
            ],
            ["educacion", "Educación / Pedagogía"],
            ["arte_diseno", "Arte / Diseño / Arquitectura"],
            ["otra", "Otra"],
        ],
        widget=widgets.RadioSelect,
    )
    works = models.BooleanField(
        label="¿Actualmente trabajas?",
        choices=[[True, "Sí"], [False, "No"]],
        widget=widgets.RadioSelect,
    )
    used_guardaditos = models.BooleanField(
        label='¿Has usado alguna vez "WARDADITOS" del BCP?',
        choices=[[True, "Sí"], [False, "No"]],
        widget=widgets.RadioSelect,
    )

    # ── Variables del experimento
    income = models.IntegerField()
    automatic_saving = models.FloatField(initial=0)
    manual_saving = models.FloatField(min=0)
    consumption = models.FloatField(min=0)
    savings_balance = models.FloatField(initial=0)
    liquid_balance = models.FloatField(initial=0)


# ── Hook de creación de sesión
def creating_session(subsession: Subsession):

    subsession.round_income = random.randint(C.MIN_INCOME, C.MAX_INCOME)

    for player in subsession.get_players():
        participant = player.participant
        if subsession.round_number == 1:
            participant.treatment = random.choice([0, 1])

        player.treatment = participant.treatment
        player.income = subsession.round_income


# PAGINAS
class Sociodemografica(Page):
    """
    Encuesta sociodemográfica. Solo se muestra en la ronda 1,
    antes de las instrucciones del experimento.
    """

    form_model = "player"
    form_fields = [
        "age",
        "gender",
        "university",
        "career",
        "works",
        "used_guardaditos",
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1


class Instructions(Page):
    form_model = "player"

    @staticmethod
    def is_displayed(player: Player):

        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):

        return dict(treatment=player.treatment)


class Decision(Page):
    form_model = "player"
    form_fields = ["manual_saving", "consumption"]

    @staticmethod
    def vars_for_template(player: Player):

        automatic_saving = (
            round(C.DEFAULT_RATE * player.income, 2) if player.treatment == 1 else 0
        )
        available_income = player.income - automatic_saving
        return dict(
            treatment=player.treatment,
            income=player.income,
            automatic_saving=automatic_saving,
            available_income=available_income,
            is_shock_round=player.round_number == C.SHOCK_ROUND,
        )

    @staticmethod
    def error_message(player: Player, values):

        automatic_saving = (
            C.DEFAULT_RATE * player.income if player.treatment == 1 else 0
        )
        available_income = player.income - automatic_saving
        total_spending = values["manual_saving"] + values["consumption"]

        if total_spending > available_income:
            return "No puedes gastar y ahorrar más que tu ingreso disponible."


class Results(Page):
    form_model = "player"

    @staticmethod
    def vars_for_template(player: Player):

        return dict(
            is_shock_round=player.round_number == C.SHOCK_ROUND,
        )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):

        if player.treatment == 1:
            player.automatic_saving = round(C.DEFAULT_RATE * player.income, 2)
        else:
            player.automatic_saving = 0

        total_saving = player.manual_saving + player.automatic_saving

        if player.round_number == 1:
            previous_savings = 0
        else:
            previous_savings = player.in_round(player.round_number - 1).savings_balance

        player.savings_balance = previous_savings + total_saving
        player.liquid_balance = player.income - total_saving - player.consumption

        # El shock reduce el balance líquido; puede quedar negativo
        # (deuda / penalidad implícita que el participante debe absorber)
        if player.round_number == C.SHOCK_ROUND:
            player.liquid_balance -= C.SHOCK_AMOUNT


page_sequence = [Sociodemografica, Instructions, Decision, Results]
