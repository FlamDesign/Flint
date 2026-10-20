"""Catalog data for the Flint demo storefront.

Edit products here, then run `python3 build.py` to regenerate every page,
products.json, feed.xml and sitemap.xml.
"""

STORE = {
    "name": "Flint",
    "tagline": "Made to be picked up.",
    "currency": "USD",
    "description": "A small, considered collection of things to wear, carry, write with, build and keep.",
}

# Shared colour values (label, swatch hex)
EMBER = ("Ember", "#C9532A")
INK = ("Ink", "#22211F")
BONE = ("Bone", "#E8E1D4")
ASH = ("Ash", "#A3A19C")
NATURAL = ("Natural", "#D9CDB4")
CHARCOAL = ("Charcoal", "#4A4947")
BRASS = ("Brass", "#B8955A")
BLACK = ("Black", "#2A2A2A")

APPAREL_SIZES = ["XS", "S", "M", "L", "XL", "XXL"]

CATEGORIES = [
    ("wear", "Wear", "Heavyweight basics, cut a little boxy and built to soften with every wash."),
    ("carry", "Carry", "Bags and sleeves for the things you take between rooms and cities."),
    ("desk", "Desk", "Tools for writing things down before they disappear."),
    ("home", "Home", "Things to drink from and light up at the end of a long day."),
    ("play", "Play", "Build sets, pins and stickers. Small objects with no job but joy."),
]

EDITORIAL = {
    "wear": ["ed-wear", "ed-hero"],
    "carry": ["ed-wear"],
    "desk": ["ed-desk", "ed-flatlay"],
    "home": ["ed-home"],
    "play": ["ed-desk", "ed-flatlay"],
}


def v(color, img, price=None, note=None):
    out = {"label": color[0], "hex": color[1], "img": img}
    if price is not None:
        out["price"] = price
    if note:
        out["note"] = note
    return out


PRODUCTS = [
    {
        "slug": "heavyweight-hoodie", "sku": "HOOD", "name": "Heavyweight Hoodie", "category": "wear",
        "price": 88, "badge": "Bestseller",
        "summary": "A 480gsm brushed fleece hoodie with a boxy body, dropped shoulders and a small embroidered spark on the chest.",
        "details": ["480gsm brushed-back cotton fleece", "Boxy fit with dropped shoulders", "Double-layer hood, no drawcords", "Tonal embroidered spark on left chest", "Garment dyed for a soft, lived-in hand"],
        "materials": "100% organic cotton. Knitted and garment dyed in Portugal.",
        "care": "Wash cold inside out. Hang dry. Pre-shrunk, but it still loves a low tumble.",
        "option": "Color", "values": [v(EMBER, "hoodie-ember"), v(INK, "hoodie-ink"), v(BONE, "hoodie-bone")],
        "sizes": APPAREL_SIZES,
    },
    {
        "slug": "boxy-tee", "sku": "TEE", "name": "Boxy Tee", "category": "wear", "price": 38, "badge": "New",
        "summary": "A dense 260gsm jersey tee with a cropped boxy cut and a tight ribbed collar that keeps its shape.",
        "details": ["260gsm combed cotton jersey", "Cropped, boxy silhouette", "1.5cm ribbed collar", "Printed spark on left chest"],
        "materials": "100% combed cotton.",
        "care": "Wash cold. Tumble dry low. Iron inside out.",
        "option": "Color", "values": [v(BONE, "tee-bone"), v(INK, "tee-ink")],
        "sizes": APPAREL_SIZES,
    },
    {
        "slug": "loopback-crew", "sku": "CREW", "name": "Loopback Crew", "category": "wear", "price": 78,
        "summary": "An unbrushed loopback crewneck with a quiet embroidered wordmark. Lighter than the hoodie, made for in-between weather.",
        "details": ["400gsm loopback terry", "Regular fit, ribbed cuffs and hem", "Embroidered wordmark across the chest", "Flatlock seams"],
        "materials": "100% organic cotton.",
        "care": "Wash cold inside out. Hang dry.",
        "option": "Color", "values": [v(ASH, "crew-ash"), v(EMBER, "crew-ember")],
        "sizes": APPAREL_SIZES,
    },
    {
        "slug": "six-panel-cap", "sku": "CAP", "name": "Six-Panel Cap", "category": "wear", "price": 34,
        "summary": "An unstructured washed twill cap with a low crown and a spark stitched on the front.",
        "details": ["Washed cotton twill", "Unstructured, low-profile crown", "Brass slider strap", "Embroidered spark"],
        "materials": "100% cotton twill.",
        "care": "Spot clean. Reshape while damp.",
        "option": "Color", "values": [v(INK, "cap-ink"), v(BONE, "cap-bone"), v(EMBER, "cap-ember")],
        "sizes": ["One size"],
    },
    {
        "slug": "rib-beanie", "sku": "BEAN", "name": "Rib Beanie", "category": "wear", "price": 32,
        "summary": "A chunky merino rib beanie with a deep cuff and a small woven label.",
        "details": ["Extra-fine merino wool", "2x2 chunky rib", "Deep fold-over cuff", "Woven spark label"],
        "materials": "100% extra-fine merino wool. Knitted in Scotland.",
        "care": "Hand wash cold. Dry flat.",
        "option": "Color", "values": [v(EMBER, "beanie-ember"), v(INK, "beanie-ink")],
        "sizes": ["One size"],
    },
    {
        "slug": "canvas-tote", "sku": "TOTE", "name": "Canvas Tote", "category": "carry", "price": 28,
        "summary": "A 16oz canvas tote with long handles, an inside pocket and a small screen print near the base.",
        "details": ["16oz heavyweight cotton canvas", "Long handles for shoulder carry", "Inside slip pocket", "Screen printed in water-based ink"],
        "materials": "100% cotton canvas.",
        "care": "Spot clean or cold hand wash.",
        "option": "Color", "values": [v(NATURAL, "tote-natural"), v(INK, "tote-ink")],
    },
    {
        "slug": "felt-laptop-sleeve", "sku": "SLV", "name": "Felt Laptop Sleeve", "category": "carry", "price": 54,
        "summary": "A thick wool felt sleeve with a leather pull tab. Fits most 13 and 14 inch laptops.",
        "details": ["5mm pressed wool felt", "Vegetable-tanned leather pull tab", "Debossed spark on tab", "Fits laptops up to 31.5 x 22.5cm"],
        "materials": "Merino wool felt, vegetable-tanned leather.",
        "care": "Brush clean. Keep leather away from water.",
        "option": "Color", "values": [v(CHARCOAL, "sleeve-charcoal"), v(EMBER, "sleeve-ember")],
    },
    {
        "slug": "machined-pen", "sku": "PEN", "name": "Machined Pen", "category": "desk", "price": 64, "badge": "Limited",
        "summary": "A weighty ballpoint turned from solid bar stock, with a knurled grip and a tiny engraved spark.",
        "details": ["CNC machined from solid bar", "Knurled grip, pocket clip", "Takes standard Parker-style refills", "Engraved spark near the clip"],
        "materials": "Solid brass, or aluminum with black anodized finish.",
        "care": "Brass develops a patina. Polish to restore, or let it age.",
        "option": "Finish", "values": [v(BRASS, "pen-brass", 64), v(BLACK, "pen-black", 58)],
    },
    {
        "slug": "gel-pen-trio", "sku": "GEL", "name": "Gel Pen Trio", "category": "desk", "price": 16,
        "summary": "Three slim 0.5mm gel pens in the house colors. Smooth, quick-drying, refillable.",
        "details": ["Set of three, 0.5mm tip", "Quick-drying black gel ink", "Refillable", "Matte barrels"],
        "materials": "Recycled ABS barrels.",
        "care": "Cap after use.",
        "option": "Set", "values": [{"label": "Ember, Ink, Bone", "hex": "#C9532A", "img": "gelpens"}],
    },
    {
        "slug": "lay-flat-notebook", "sku": "NB", "name": "Lay-Flat Notebook", "category": "desk", "price": 24,
        "summary": "An A5 dot-grid notebook with exposed binding, so every spread opens perfectly flat.",
        "details": ["A5, 192 pages", "100gsm dot-grid paper", "Exposed Swiss binding, opens flat", "Linen cloth cover"],
        "materials": "FSC-certified paper, bookcloth cover.",
        "care": "Keep dry.",
        "option": "Color", "values": [v(EMBER, "notebook-ember"), v(INK, "notebook-ink"), v(BONE, "notebook-bone")],
    },
    {
        "slug": "felt-desk-mat", "sku": "MAT", "name": "Felt Desk Mat", "category": "desk", "price": 48,
        "summary": "A wide wool felt mat with a natural cork base. Quiet under a keyboard, soft under a forearm.",
        "details": ["90 x 40cm", "3mm wool felt top", "Natural cork base, non-slip", "Stitched spark in the corner"],
        "materials": "Merino wool felt, natural cork.",
        "care": "Lint roll. Spot clean.",
        "option": "Color", "values": [v(INK, "deskmat-ink"), v(EMBER, "deskmat-ember")],
    },
    {
        "slug": "stoneware-mug", "sku": "MUG", "name": "Stoneware Mug", "category": "home", "price": 30,
        "summary": "A thrown stoneware mug with a satin glaze and a raw clay foot. Holds a proper 350ml.",
        "details": ["350ml", "Hand thrown stoneware", "Satin glaze, raw clay foot", "Dishwasher and microwave safe"],
        "materials": "Speckled stoneware clay.",
        "care": "Dishwasher safe. Each piece varies slightly.",
        "option": "Color", "values": [v(BONE, "mug-bone"), v(INK, "mug-ink")],
    },
    {
        "slug": "insulated-bottle", "sku": "BTL", "name": "Insulated Bottle", "category": "home", "price": 36,
        "summary": "A 750ml double-wall steel bottle with a powder-coated finish. Cold for 24 hours, hot for 12.",
        "details": ["750ml capacity", "Double-wall vacuum insulation", "Powder-coated, grippy finish", "Leakproof steel cap with loop"],
        "materials": "18/8 stainless steel.",
        "care": "Hand wash only.",
        "option": "Color", "values": [v(EMBER, "bottle-ember"), v(INK, "bottle-ink"), v(BONE, "bottle-bone")],
    },
    {
        "slug": "soy-candle", "sku": "CDL", "name": "Soy Candle", "category": "home", "price": 42, "badge": "New",
        "summary": "A 220g soy candle with a crackling wooden wick. Two scents for the end of the day.",
        "details": ["220g, around 45 hours burn", "Crackling wooden wick", "Reusable glass tumbler with lid", "Ember: cedar, amber, smoked vanilla. Smoke: vetiver, black tea, birch tar"],
        "materials": "Soy wax, phthalate-free fragrance.",
        "care": "Trim the wick before each burn. Never leave unattended.",
        "option": "Scent", "values": [v(("Ember", "#B86A2C"), "candle-ember"), v(("Smoke", "#2E2C2A"), "candle-smoke")],
    },
    {
        "slug": "build-set", "sku": "BLD", "name": "Build Set", "category": "play", "price": 39, "badge": "Limited",
        "summary": "Interlocking brick builds designed in house. Start with the campfire, or go big with the two-storey studio.",
        "details": ["Compatible with major brick systems", "Printed instruction booklet", "Ages 10 and up", "Campfire: 214 pieces. Studio: 486 pieces with a light-up sign"],
        "materials": "ABS plastic bricks, recycled card box.",
        "care": "Dust with a soft brush.",
        "option": "Edition",
        "values": [
            {"label": "Campfire", "hex": "#E07A2E", "img": "bricks-campfire", "price": 39, "note": "214 pieces"},
            {"label": "Studio", "hex": "#2B2A28", "img": "bricks-studio", "price": 89, "note": "486 pieces"},
        ],
    },
    {
        "slug": "enamel-pin-set", "sku": "PIN", "name": "Enamel Pin Set", "category": "play", "price": 22,
        "summary": "Four hard enamel pins with gold-plated outlines and double rubber clutches.",
        "details": ["Set of four", "Hard enamel, gold-plated", "Around 20mm each", "Double clutch backs"],
        "materials": "Zinc alloy, enamel.",
        "care": "Wipe clean.",
        "option": "Set", "values": [{"label": "Set of four", "hex": "#C9532A", "img": "pins"}],
    },
    {
        "slug": "sticker-sheet", "sku": "STK", "name": "Sticker Sheet", "category": "play", "price": 8,
        "summary": "Ten die-cut vinyl stickers for laptops, bottles and notebooks.",
        "details": ["Ten die-cut stickers", "Matte waterproof vinyl", "UV resistant", "A5 sheet"],
        "materials": "Matte vinyl.",
        "care": "Apply to clean, dry surfaces.",
        "option": "Set", "values": [{"label": "Sheet of ten", "hex": "#C9532A", "img": "stickers"}],
    },
]
