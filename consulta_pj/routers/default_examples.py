from fastapi.openapi.models import Example

ACTORES_EXAMPLES: dict[str, Example] = {
    "0968599020001": Example(value="0968599020001"),
    "0992339411001": Example(value="0992339411001"),
    "1722218474": Example(value="1722218474"),
    "1104998453": Example(value="1104998453"),
}

DEMANDADOS_EXAMPLES = {
    "1791251237001": {"value": "1791251237001"},
    "0968599020001": {"value": "0968599020001"},
    "1104998453": {"value": "1104998453"},
}

PROCESOS_EXAMPLES = {"Actor": {"value": "02331202200019"}, "Demandado": {"value": "17230202115775"}}

CAUSA_EXAMPLE = {"Actor": {"value": "1722218474"}, "Demandado": {"value": "1104998453"}}

MOVIMIENTO_EXAMPLE = {"Actor (1722218474)": {"value": 25957977}, "Demandado (1104998453)": {"value": 14767707}}
