"""
Saisie de texte avec les yeux (Morse a 3 symboles)

  blink        (0.25 a 0.75 s)  ->  '.'
  long blink   (0.75 a 2 s)     ->  '_'
  fermeture    (plus de 2 s)    ->  efface le dernier symbole
  regard cote  (plus de 0.3 s) ->  '[]' fin de lettre
  deux '[]' de suite           ->  espace entre deux mots
"""

# ================= REGLAGES =================

CANAL_BLINK = 'eyeBlinkLeft'
CANAL_LOOK = 'eyeLookInLeft'

SEUIL_BLINK = 0.3
SEUIL_LOOK = 0.1

MIN_BLINK = 0.2
SEUIL_LONG = 0.75
EFFACER = 2.0
MIN_LOOK = 0.5

ESPACE = '[]'


# ============ TABLEAUX DE CORRESPONDANCE ============

CODES = [
    '._', '_...', '_._.', '_..', '.', '.._.', '__.',
    '....', '..', '.___', '_._', '._..', '__', '_.',
    '___', '.__.', '__._', '._.', '...', '_', '.._',
    '..._', '.__', '_.._', '_.__', '__..'
]

LETTRES = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G',
    'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U',
    'V', 'W', 'X', 'Y', 'Z'
]


# ================= OUTILS =================

def valeur(nom):
    """Lit la valeur d'un canal dans null4."""
    for c in op('null4').chans():
        if nom in c.name:
            return c.eval()
    return None


def lettre(morceau):
    """Convertit un code Morse en lettre."""
    if morceau in CODES:
        return LETTRES[CODES.index(morceau)]
    return '?'


def afficher(flux):
    """Decode les lettres et affiche la phrase dans text1."""

    texte = ''
    debut = 0

    for fin, sym in enumerate(flux):

        if sym == ESPACE:

            morceau = ''.join(flux[debut:fin])

            if morceau:
                texte += lettre(morceau)
            else:
                texte += ' '

            debut = fin + 1

    # Affiche uniquement la phrase decodee
    op('text1').par.text = texte


# ================= LOGIQUE PRINCIPALE =================

def traiter():

    s = me.storage

    # Evite de traiter deux fois la meme image
    if s.get('image') == absTime.frame:
        return

    s['image'] = absTime.frame

    b = valeur(CANAL_BLINK)
    l = valeur(CANAL_LOOK)

    if b is None or l is None:
        op('text1').par.text = 'Canaux introuvables dans null4'
        return

    now = absTime.seconds

    s.setdefault('flux', [])
    s.setdefault('ferme', False)
    s.setdefault('t_ferme', now)
    s.setdefault('look', False)
    s.setdefault('t_look', now)
    s.setdefault('look_compte', False)

    flux = s['flux']


    # ----------- CLIGNEMENTS -----------

    ferme = b > SEUIL_BLINK

    if ferme and not s['ferme']:
        s['t_ferme'] = now

    if not ferme and s['ferme']:

        d = now - s['t_ferme']

        if d >= EFFACER:

            # Efface le dernier symbole
            if flux:
                flux.pop()

        elif d >= SEUIL_LONG:

            # Ajoute un trait
            flux.append('_')

        elif d >= MIN_BLINK:

            # Ajoute un point
            flux.append('.')

    s['ferme'] = ferme


    # ----------- REGARD SUR LE COTE -----------

    look = l > SEUIL_LOOK and not ferme

    if look and not s['look']:
        s['t_look'] = now
        s['look_compte'] = False

    if look and not s['look_compte'] and now - s['t_look'] >= MIN_LOOK:

        # Termine une lettre
        flux.append(ESPACE)

        s['look_compte'] = True

    s['look'] = look

    s['flux'] = flux

    # Met a jour le Text TOP
    afficher(flux)


# ============ POINTS D'ENTREE TOUCHDESIGNER ============

def onFrameEnd(frame):
    """Execute DAT : Frame End active."""
    traiter()
    return


def onValueChange(channel, sampleIndex, val, prev):
    """CHOP Execute DAT : Value Change active."""
    traiter()
    return