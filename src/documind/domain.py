"""Entidades del dominio de DocuMind y reglas de fragmentación de texto."""

from collections.abc import Iterator
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Fragmento:
    """Un pedazo de texto de un documento: la unidad que se busca en el RAG."""

    texto: str
    posicion: int  # orden dentro del documento: 0, 1, 2...
    documento_id: int | None = None  # None hasta que se guarde en la BD


@dataclass(frozen=True)
class Documento:
    """Un documento completo subido por el usuario."""

    titulo: str
    contenido: str
    id: int | None = None
    creado: datetime = field(default_factory=datetime.now)

    def fragmentar(self, tamaño: int = 500, solapamiento: int = 50) -> list[Fragmento]:
        """Convierte el contenido en una lista de Fragmento numerados."""
        return [
            Fragmento(texto=t, posicion=i, documento_id=self.id)
            for i, t in enumerate(dividir_en_fragmentos(self.contenido, tamaño, solapamiento))
        ]


def dividir_en_fragmentos(texto: str, tamaño: int = 500, solapamiento: int = 50) -> Iterator[str]:
    """Genera trozos de `tamaño` caracteres que se solapan `solapamiento` caracteres."""
    if tamaño <= 0:
        raise ValueError("tamaño debe ser mayor que 0")
    if not 0 <= solapamiento < tamaño:
        raise ValueError("solapamiento debe estar entre 0 y tamaño - 1")

    texto = texto.strip()
    paso = tamaño - solapamiento
    inicio = 0
    while inicio < len(texto):
        fin = inicio + tamaño
        yield texto[inicio:fin]
        if fin >= len(texto):  # ya llegamos al final: no generar un trozo repetido
            break
        inicio += paso
