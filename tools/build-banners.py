"""Generate the SumProduct GitHub profile banners.

Both the light-theme and dark-theme banners are produced from this single source so the
pair can never drift apart. Re-run after any edit:

    python tools/build-banners.py

Brand references (sp_brand_guidelines_v1.02CE, May 2026):
  p3   logo must never be recreated in a substitute font -- the wordmark below is the
       original vector outline lifted from the guidelines cover, not type.
  p6   logo sits in the top-left corner.
  p14  palette and the 45-degree linear gradient rule.
  p17  mathematical symbols are the brand's visual DNA, kept faint so layouts stay calm.
"""
from pathlib import Path

# --- palette (p14) ---------------------------------------------------------------
DARK_GREEN = "#1e3c3b"
GREEN = "#007033"
LIME = "#d2f7b1"
BLACK = "#000000"
WHITE = "#ffffff"

# --- canvas ----------------------------------------------------------------------
W, H = 1200, 320
PAD = 64                      # left margin, also the logo's clear space (p4)
STRIP = 64                    # right-edge colour block, echoing the guidelines cover

# --- wordmark --------------------------------------------------------------------
# Original vector outline, extracted from page 1 of the brand guidelines.
LOGO_W, LOGO_H = 123.78, 49.25
LOGO_D = Path(__file__).with_name("wordmark.path").read_text(encoding="utf8").strip()

# Type stack degrades to Arial, which is itself an approved brand face (p16),
# so the banner stays on-brand even where DM Sans is unavailable.
FONT = "'DM Sans','DM Sans 9pt',Inter,'Segoe UI',Arial,Helvetica,sans-serif"

# Faint mathematical motif: (glyph, x, y, size, opacity)
SYMBOLS = [
    ("Σ", 596, 132, 118, 0.055),   # sigma
    ("√", 830, 126, 92, 0.05),     # root
    ("÷", 726, 258, 74, 0.06),     # divide
    ("π", 902, 304, 300, 0.07),    # pi
    ("×", 1058, 178, 112, 0.055),  # multiply
]


def symbol_layer():
    out = []
    for glyph, x, y, size, op in SYMBOLS:
        out.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="700" fill="{WHITE}" fill-opacity="{op}" '
            f'text-anchor="middle">{glyph}</text>'
        )
    return "\n    ".join(out)


def banner(theme):
    """theme: 'light' uses the Green-to-Dark-Green gradient, 'dark' Dark-Green-to-Black (p14)."""
    if theme == "light":
        c0, c1 = GREEN, DARK_GREEN
    else:
        c0, c1 = DARK_GREEN, BLACK

    scale = 64 / LOGO_H                       # render the wordmark 64px tall
    logo_y = 68

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="SumProduct — Excel and data analytics consultancy">
  <title>SumProduct — Excel and data analytics consultancy</title>
  <defs>
    <linearGradient id="bg" x1="0" y1="1" x2="1" y2="0">
      <stop offset="0" stop-color="{c0}"/>
      <stop offset="1" stop-color="{c1}"/>
    </linearGradient>
    <clipPath id="frame"><rect width="{W}" height="{H}"/></clipPath>
  </defs>

  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>

    <!-- mathematical motif: the brand's visual DNA, held faint (p17) -->
    {symbol_layer()}

    <!-- oversized chevron, echoing the guidelines cover -->
    <path d="M300 -40 L470 160 L300 360" fill="none" stroke="{WHITE}"
          stroke-opacity="0.05" stroke-width="54" stroke-linejoin="round" stroke-linecap="round"/>

    <!-- right-edge colour blocks -->
    <rect x="{W - STRIP}" y="0" width="{STRIP}" height="96" fill="{LIME}"/>
    <rect x="{W - STRIP}" y="96" width="{STRIP}" height="{H - 96}" fill="{BLACK}" fill-opacity="0.85"/>

    <!-- wordmark: original outlines, never re-typed (p3) -->
    <g transform="translate({PAD},{logo_y}) scale({scale:.5f})">
      <path d="{LOGO_D}" fill="{WHITE}" fill-rule="evenodd"/>
    </g>

    <!-- lime rule -->
    <rect x="{PAD}" y="172" width="76" height="5" fill="{LIME}"/>

    <text x="{PAD}" y="222" font-family="{FONT}" font-size="30" font-weight="700" fill="{WHITE}">
      Excel and data analytics consultancy
    </text>
    <text x="{PAD}" y="258" font-family="{FONT}" font-size="17" font-weight="400" fill="{WHITE}" fill-opacity="0.72">
      Modelling · Consulting · Strategy · Training · AI · Auditing
    </text>
    <text x="{PAD}" y="292" font-family="{FONT}" font-size="15" font-weight="700" fill="{LIME}">
      sumproduct.com
    </text>
  </g>
</svg>
"""


assets = Path(__file__).resolve().parents[1] / "profile" / "assets"
assets.mkdir(parents=True, exist_ok=True)

for theme in ("light", "dark"):
    target = assets / f"banner-{theme}.svg"
    target.write_text(banner(theme), encoding="utf8")
    print(f"wrote {target.relative_to(assets.parents[2])}  ({target.stat().st_size:,} bytes)")

# standalone wordmark, for reuse anywhere the logo is needed on a dark background
wordmark = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {LOGO_W} {LOGO_H}" '
    f'width="{LOGO_W}" height="{LOGO_H}" role="img" aria-label="SumProduct">'
    f'<path d="{LOGO_D}" fill="currentColor" fill-rule="evenodd"/></svg>\n'
)
(assets / "logo-wordmark.svg").write_text(wordmark, encoding="utf8")
print(f"wrote profile/assets/logo-wordmark.svg  ({len(wordmark):,} bytes)")
