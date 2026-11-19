"""
Paletas de seaborn/matplotlib basadas en los colores de theme.py.
Solo colores: no modifica fondos, fuentes, grillas ni rcParams de estilo.

Uso:
    import theme_sns as tsns          # registra las paletas al importar
    sns.displot(..., palette="pitch_seq")             # secuencial por nombre
    sns.heatmap(..., cmap="pitch_div")                # divergente por nombre
    sns.scatterplot(..., palette=tsns.pitch_palette(3))  # cualitativa
"""
import matplotlib as mpl
from matplotlib.colors import LinearSegmentedColormap
import seaborn as sns

from theme import PITCH_DARK, WHITE, GOLD, PALETTE


def pitch_palette(n: int | None = None) -> list:
    """Paleta CUALITATIVA (categorías sin orden).
    n=None devuelve todos los colores; si n > len(PALETTE) interpola."""
    base = list(PALETTE)
    if n is None or n == len(base):
        return base
    if n < len(base):
        return base[:n]
    return sns.blend_palette(base, n_colors=n)


def pitch_seq(n: int | None = None, reverse: bool = False):
    """Paleta SECUENCIAL: de PITCH_DARK a GOLD.
    n=None devuelve el colormap continuo; con n devuelve lista de n colores."""
    colores = [PITCH_DARK, GOLD]
    if reverse:
        colores = colores[::-1]
    return sns.blend_palette(colores, n_colors=n, as_cmap=(n is None))


def pitch_div(n: int | None = None):
    """Paleta DIVERGENTE: PITCH_DARK <- WHITE -> GOLD (centro neutro)."""
    return sns.blend_palette([PITCH_DARK, WHITE, GOLD],
                             n_colors=n, as_cmap=(n is None))


def set_palette_pitch(n: int | None = None) -> None:
    """Fija PALETTE como ciclo de colores por defecto (solo colores)."""
    sns.set_palette(pitch_palette(n))


def _register() -> None:
    """Registra colormaps para usarlos por nombre: palette="pitch_seq"."""
    for nombre, cmap in {
        "pitch_seq": pitch_seq(),
        "pitch_seq_r": pitch_seq(reverse=True),
        "pitch_div": pitch_div(),
    }.items():
        mpl.colormaps.register(
            LinearSegmentedColormap.from_list(nombre, cmap(range(256))),
            name=nombre, force=True,
        )


_register()


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    diamonds = sns.load_dataset("diamonds")

    # Ejemplo: tu gráfico original, ahora con la paleta secuencial propia
    sns.set_theme(style="whitegrid")
    sns.displot(
        data=diamonds, x="carat", hue="cut",
        kind="kde", height=6, multiple="fill", clip=(0, None),
        palette="pitch_seq",
    )

    # Vista previa de las tres familias
    fig, axes = plt.subplots(3, 1, figsize=(8, 2))
    for ax, (nombre, pal) in zip(axes, {
        "cualitativa": pitch_palette(),
        "secuencial": pitch_seq(8),
        "divergente": pitch_div(8),
    }.items()):
        sns.palplot(pal, ax=ax) if False else ax.imshow(
            [list(range(len(pal)))],
            cmap=sns.blend_palette(pal, as_cmap=True), aspect="auto")
        ax.set_xticks([]); ax.set_yticks([])
        ax.set_ylabel(nombre, rotation=0, ha="right", va="center")