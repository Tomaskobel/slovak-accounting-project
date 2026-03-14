"""
AI klasifikátor transakcií — Layer 3 classification for the deterministic engine.

Takes unstructured transaction description (text, invoice data) and classifies it
into structured Transakcia fields that the engine can process.

Flow:
  user input → AI classifier → Transakcia → deterministic engine → journal entry
                    ↓
              if uncertain → human review

No AI in the posting path. AI only classifies, then hands off to motor.py.
"""

import logging
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Optional

import anthropic
from dotenv import load_dotenv

from engine.motor import Transakcia, zauctuj, UctovnyZapis
from engine.schema import (
    SmerTransakcie, TypPlnenia, KrajinaDodavatela,
)

load_dotenv(override=True)

logger = logging.getLogger(__name__)


class KlasifikaciaVysledok(str, Enum):
    """Result of classification attempt."""
    USPESNA = "uspesna"           # Confident classification → engine
    NEISTA = "neista"             # Uncertain → present options to user
    NEZNAMA = "neznama"           # Cannot classify → route to accountant


@dataclass
class Klasifikacia:
    """AI classification output."""
    vysledok: KlasifikaciaVysledok
    transakcia: Optional[Transakcia]
    dovera: float                    # 0.0 - 1.0 confidence score
    zdovodnenie: str                 # Slovak explanation of classification
    alternativy: Optional[list[dict]] = None   # Alternative classifications if uncertain
    pravidlo_id: Optional[str] = None  # Matched rule ID (if uspesna)


# ---------------------------------------------------------------------------
# System prompt — regulatory context for classification
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """Si klasifikátor účtovných transakcií pre slovenské s.r.o. (podvojné účtovníctvo).

Tvoja úloha: z popisu transakcie určiť štruktúrované polia pre účtovný motor.

Polia na klasifikáciu:
- smer: "nakup" | "predaj" | "oprava" | "preddavok"
- typ_plnenia: "tovar" | "sluzba" | "material" | "dhm" | "energia" | null
- krajina_dodavatela: "SK" | "EU" | "non_EU"
- platitel_dph_kupujuci: true | false | null
- platitel_dph_dodavatel: true | false | null
- forma_uhrady: "faktura" | "hotovost" | "preddavok" | "banka" | null
- metoda_zasob: "A" | "B" | null
- tuzemsky_prenos: true | false | null

Sumy:
- zaklad_dane: základ dane (bez DPH)
- celkova_suma: celková suma (vrátane DPH) — len pre transakcie bez DPH
- sadzba_dane: sadzba DPH (23, 19, 5, 0)
- nadobudacia_cena: obstarávacia cena (COGS, clo)
- preddavkova_suma: suma preddavku

Pravidlá:
1. Ak máš istotu ≥ 0.8, klasifikuj priamo
2. Ak máš istotu 0.5-0.8, ponúkni hlavnú klasifikáciu + alternatívy
3. Ak máš istotu < 0.5, označ ako "neznama" a odporúč konzultáciu s účtovníkom

Vždy uveď zdôvodnenie po slovensky.

Kontext: Slovenské DPH sadzby od 2025: 23% (základná), 19% (znížená), 5% (znížená II).
Tuzemský prenos: § 69 ods. 12 — stavebné práce, elektronika >5000 EUR.
"""

CLASSIFICATION_TOOL = {
    "name": "klasifikuj_transakciu",
    "description": "Klasifikuj transakciu do štruktúrovaných polí pre účtovný motor",
    "input_schema": {
        "type": "object",
        "properties": {
            "dovera": {
                "type": "number",
                "description": "Úroveň istoty 0.0-1.0",
                "minimum": 0.0,
                "maximum": 1.0,
            },
            "zdovodnenie": {
                "type": "string",
                "description": "Zdôvodnenie klasifikácie (po slovensky)",
            },
            "smer": {
                "type": "string",
                "enum": ["nakup", "predaj", "oprava", "preddavok"],
            },
            "typ_plnenia": {
                "type": ["string", "null"],
                "enum": ["tovar", "sluzba", "material", "dhm", "energia", None],
            },
            "krajina_dodavatela": {
                "type": "string",
                "enum": ["SK", "EU", "non_EU"],
            },
            "platitel_dph_kupujuci": {"type": ["boolean", "null"]},
            "platitel_dph_dodavatel": {"type": ["boolean", "null"]},
            "forma_uhrady": {
                "type": ["string", "null"],
                "enum": ["faktura", "hotovost", "preddavok", "banka", None],
            },
            "metoda_zasob": {
                "type": ["string", "null"],
                "enum": ["A", "B", None],
            },
            "tuzemsky_prenos": {"type": ["boolean", "null"]},
            "zaklad_dane": {"type": ["number", "null"]},
            "celkova_suma": {"type": ["number", "null"]},
            "sadzba_dane": {"type": ["number", "null"]},
            "nadobudacia_cena": {"type": ["number", "null"]},
            "preddavkova_suma": {"type": ["number", "null"]},
            "alternativy": {
                "type": ["array", "null"],
                "description": "Alternatívne klasifikácie ak istota < 0.8",
                "items": {
                    "type": "object",
                    "properties": {
                        "smer": {"type": "string"},
                        "typ_plnenia": {"type": ["string", "null"]},
                        "dovera": {"type": "number"},
                        "zdovodnenie": {"type": "string"},
                    },
                },
            },
        },
        "required": ["dovera", "zdovodnenie", "smer", "krajina_dodavatela"],
    },
}


def _build_transakcia(data: dict) -> Transakcia:
    """Convert AI classification output to Transakcia dataclass."""
    smer_map = {v.value: v for v in SmerTransakcie}
    typ_map = {v.value: v for v in TypPlnenia}
    krajina_map = {v.value: v for v in KrajinaDodavatela}

    return Transakcia(
        smer=smer_map[data["smer"]],
        typ_plnenia=typ_map.get(str(data["typ_plnenia"])) if data.get("typ_plnenia") else None,
        krajina_dodavatela=krajina_map[data["krajina_dodavatela"]],
        platitel_dph_kupujuci=data.get("platitel_dph_kupujuci"),
        platitel_dph_dodavatel=data.get("platitel_dph_dodavatel"),
        forma_uhrady=data.get("forma_uhrady"),
        metoda_zasob=data.get("metoda_zasob"),
        tuzemsky_prenos=data.get("tuzemsky_prenos"),
        zaklad_dane=Decimal(str(data["zaklad_dane"])) if data.get("zaklad_dane") is not None else None,
        celkova_suma=Decimal(str(data["celkova_suma"])) if data.get("celkova_suma") is not None else None,
        sadzba_dane=Decimal(str(data["sadzba_dane"])) if data.get("sadzba_dane") is not None else None,
        nadobudacia_cena=Decimal(str(data["nadobudacia_cena"])) if data.get("nadobudacia_cena") is not None else None,
        preddavkova_suma=Decimal(str(data["preddavkova_suma"])) if data.get("preddavkova_suma") is not None else None,
    )


def klasifikuj(popis: str, kontext: Optional[str] = None) -> Klasifikacia:
    """Classify a transaction description using Claude.

    Args:
        popis: Free-text transaction description (Slovak or English).
        kontext: Optional additional context (company info, VAT status, etc.).

    Returns:
        Klasifikacia with structured result.
    """
    client = anthropic.Anthropic()

    user_message = f"Transakcia na klasifikáciu:\n{popis}"
    if kontext:
        user_message += f"\n\nDoplnkový kontext:\n{kontext}"

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        tools=[CLASSIFICATION_TOOL],  # type: ignore[list-item]
        messages=[{"role": "user", "content": user_message}],
    )

    # Extract tool use result
    tool_use = None
    for block in response.content:
        if block.type == "tool_use" and block.name == "klasifikuj_transakciu":
            tool_use = block
            break

    if not tool_use:
        logger.warning("AI did not use classification tool. Response: %s", response.content)
        return Klasifikacia(
            vysledok=KlasifikaciaVysledok.NEZNAMA,
            transakcia=None,
            dovera=0.0,
            zdovodnenie="AI nepoužil klasifikačný nástroj",
        )

    data: dict = tool_use.input  # type: ignore[assignment]
    dovera: float = float(data.get("dovera", 0.0))
    zdovodnenie: str = str(data.get("zdovodnenie", ""))
    alternativy: Optional[list[dict]] = data.get("alternativy")

    # Determine result type based on confidence
    if dovera >= 0.8:
        vysledok = KlasifikaciaVysledok.USPESNA
    elif dovera >= 0.5:
        vysledok = KlasifikaciaVysledok.NEISTA
    else:
        vysledok = KlasifikaciaVysledok.NEZNAMA

    # Build Transakcia
    transakcia = _build_transakcia(data)

    # Try to find matching rule
    pravidlo_id = None
    if vysledok == KlasifikaciaVysledok.USPESNA:
        try:
            from engine.motor import vyber_pravidlo
            pravidlo = vyber_pravidlo(transakcia)
            pravidlo_id = pravidlo.id
        except ValueError:
            # No rule matched — downgrade confidence
            vysledok = KlasifikaciaVysledok.NEISTA
            zdovodnenie += " (Žiadne pravidlo sa nezhoduje — overte klasifikáciu.)"

    return Klasifikacia(
        vysledok=vysledok,
        transakcia=transakcia,
        dovera=dovera,
        zdovodnenie=zdovodnenie,
        alternativy=alternativy,
        pravidlo_id=pravidlo_id,
    )


def klasifikuj_a_zauctuj(popis: str, kontext: Optional[str] = None) -> tuple[Klasifikacia, Optional[UctovnyZapis]]:
    """Classify and book a transaction in one step.

    Returns (classification, journal_entry) where journal_entry is None
    if classification is not confident enough.
    """
    klas = klasifikuj(popis, kontext)

    if klas.vysledok != KlasifikaciaVysledok.USPESNA or klas.transakcia is None:
        return klas, None

    try:
        zapis = zauctuj(klas.transakcia)
        return klas, zapis
    except ValueError as e:
        logger.warning("Classification succeeded but engine failed: %s", e)
        klas.vysledok = KlasifikaciaVysledok.NEISTA
        klas.zdovodnenie += f" (Motor chyba: {e})"
        return klas, None
