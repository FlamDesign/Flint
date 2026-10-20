#!/usr/bin/env python3
"""Static site generator for the Flint demo storefront.

Usage:
    python3 build.py                      # build with relative URLs
    BASE_URL=https://you.github.io/flint python3 build.py   # absolute URLs in feeds / OG tags

Images resolve to ./images/<key>.png when that file exists locally
(run scripts/fetch-images.sh once), otherwise to the hosted CDN copy.
"""
import html
import json
import os
from datetime import date
from pathlib import Path

from catalog import CATEGORIES, EDITORIAL, PRODUCTS, STORE

ROOT = Path(__file__).parent
BASE_URL = os.environ.get("BASE_URL", "").rstrip("/")
CAT = {k: (name, blurb) for k, name, blurb in CATEGORIES}
E = html.escape


# ---------------------------------------------------------------- images
def load_images():
    out = {}
    for line in (ROOT / "images.tsv").read_text().splitlines():
        if line.strip():
            _, key, url = line.split("\t")
            out[key] = url
    return out


IMAGES = load_images()


def img(key, root="", thumb=False):
    local = ROOT / "images" / f"{key}.png"
    if local.exists():
        if thumb and (ROOT / "images" / "min" / f"{key}.webp").exists():
            return f"{root}images/min/{key}.webp"
        return f"{root}images/{key}.png"
    url = IMAGES[key]
    return url.replace(".png", "_min.webp") if thumb else url


def abs_url(path):
    return f"{BASE_URL}/{path}" if BASE_URL else path


def abs_img(key):
    u = img(key)
    return u if u.startswith("http") else abs_url(u)


# ---------------------------------------------------------------- model helpers
def code(label):
    return "".join(ch for ch in label.upper() if ch.isalnum())[:3]


def variants(p):
    out = []
    for val in p["values"]:
        for size in p.get("sizes", [None]):
            sku = f"FLT-{p['sku']}-{code(val['label'])}" + (f"-{code(size)}" if size and size != "One size" else "")
            out.append({
                "sku": sku,
                p["option"].lower(): val["label"],
                **({"size": size} if size else {}),
                "price": val.get("price", p["price"]),
                "image": abs_img(val["img"]),
                "available": True,
            })
    return out


def price_range(p):
    prices = sorted({val.get("price", p["price"]) for val in p["values"]})
    return prices[0], prices[-1]


def fmt(n):
    return f"${n:,.0f}"


def price_label(p):
    lo, hi = price_range(p)
    return fmt(lo) if lo == hi else f"From {fmt(lo)}"


# ---------------------------------------------------------------- shared chrome
SPARK = '<svg class="spark" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 0C12.9 7.1 16.9 11.1 24 12C16.9 12.9 12.9 16.9 12 24C11.1 16.9 7.1 12.9 0 12C7.1 11.1 11.1 7.1 12 0Z"/></svg>'


def head(title, desc, root, og_img=None, extra=""):
    og = f'<meta property="og:image" content="{E(og_img)}">' if og_img else ""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<meta property="og:site_name" content="{STORE['name']}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
{og}
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400..700&family=Geist:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{root}assets/styles.css">
{extra}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<p class="notice">A demo storefront. Browse freely; nothing here is actually for sale.</p>
"""


def header(root, active=""):
    links = "".join(
        f'<a href="{root}shop?c={k}"{" aria-current=\"page\"" if active == k else ""}>{name}</a>'
        for k, name, _ in CATEGORIES
    )
    return f"""<header class="site-header">
  <nav class="nav-left" aria-label="Categories">
    <a href="{root}shop"{' aria-current="page"' if active == "all" else ""}>Shop all</a>
    <span class="nav-cats">{links}</span>
  </nav>
  <a class="wordmark" href="{root or './'}" aria-label="{STORE['name']} home">{SPARK}<span>{STORE['name']}</span></a>
  <div class="nav-right">
    <button class="bag-btn" type="button" data-open-cart aria-label="Open bag">Bag <span class="bag-count" data-cart-count>0</span></button>
  </div>
</header>
<aside class="cart" id="cart" aria-label="Bag" aria-hidden="true" data-root="{root}">
  <div class="cart-scrim" data-close-cart></div>
  <div class="cart-panel" role="dialog" aria-modal="true" aria-labelledby="cart-title">
    <div class="cart-head"><h2 id="cart-title">Your bag</h2><button type="button" class="link-btn" data-close-cart>Close</button></div>
    <ul class="cart-lines" data-cart-lines></ul>
    <p class="cart-empty" data-cart-empty>Your bag is empty. Pick something up from the <a href="{root}shop">shop</a>.</p>
    <div class="cart-foot" data-cart-foot>
      <div class="cart-total"><span>Subtotal</span><span data-cart-subtotal>$0</span></div>
      <button type="button" class="btn btn-solid btn-block" data-checkout>Check out</button>
      <p class="fineprint">Checkout is turned off on this demo storefront.</p>
    </div>
  </div>
</aside>
<div class="toast" role="status" aria-live="polite" data-toast></div>
"""


def footer(root):
    cols = "".join(f'<li><a href="{root}shop?c={k}">{name}</a></li>' for k, name, _ in CATEGORIES)
    return f"""<footer class="site-footer">
  <div class="foot-brand">{SPARK}<p>{STORE['name']} is a small, considered collection of things to wear, carry, write with, build and keep.</p></div>
  <div class="foot-cols">
    <div><h3>Shop</h3><ul><li><a href="{root}shop">Everything</a></li>{cols}</ul></div>
    <div><h3>Help</h3><ul><li><a href="{root}shop">Shipping</a></li><li><a href="{root}shop">Returns</a></li><li><a href="{root}shop">Size guide</a></li></ul></div>
    <div><h3>Data</h3><ul><li><a href="{root}products.json">products.json</a></li><li><a href="{root}feed.xml">Product feed</a></li><li><a href="{root}sitemap.xml">Sitemap</a></li></ul></div>
  </div>
  <p class="foot-legal">Demo storefront. Products, prices and imagery are illustrative. &copy; {date.today().year} {STORE['name']}</p>
</footer>
<script src="{root}assets/app.js" defer></script>
</body>
</html>
"""


def card(p, root, i=0):
    first = p["values"][0]
    swatches = ""
    if len(p["values"]) > 1:
        dots = "".join(f'<span class="dot" style="--c:{val["hex"]}" title="{E(val["label"])}"></span>' for val in p["values"])
        swatches = f'<span class="dots" aria-label="{len(p["values"])} {p["option"].lower()}s">{dots}</span>'
    badge = f'<span class="badge">{E(p["badge"])}</span>' if p.get("badge") else ""
    lo, _ = price_range(p)
    return f"""<article class="card" data-category="{p['category']}" data-price="{lo}" data-order="{i}" data-product-id="{p['slug']}" itemscope itemtype="https://schema.org/Product">
  <a href="{root}products/{p['slug']}" class="card-link">
    <div class="card-img">{badge}<img src="{img(first['img'], root, thumb=True)}" alt="{E(p['name'])} in {E(first['label'])}" loading="lazy" width="896" height="1120" itemprop="image"></div>
    <div class="card-meta">
      <h3 itemprop="name">{E(p['name'])}</h3>
      <p class="card-price" itemprop="offers" itemscope itemtype="https://schema.org/Offer"><meta itemprop="priceCurrency" content="USD"><meta itemprop="price" content="{lo}">{price_label(p)}</p>
      {swatches}
    </div>
  </a>
</article>"""


# ---------------------------------------------------------------- pages
def page_home():
    r = ""
    feat = [p for p in PRODUCTS if p["slug"] in (
        "heavyweight-hoodie", "machined-pen", "soy-candle", "build-set",
        "lay-flat-notebook", "six-panel-cap", "insulated-bottle", "felt-laptop-sleeve")]
    cats = ""
    for k, name, blurb in CATEGORIES:
        items = [p for p in PRODUCTS if p["category"] == k]
        thumbs = "".join(f'<img src="{img(p["values"][0]["img"], r, True)}" alt="" loading="lazy">' for p in items[:3])
        cats += f"""<li><a href="shop?c={k}" class="cat-row">
  <span class="cat-name">{name}</span>
  <span class="cat-blurb">{E(blurb)}</span>
  <span class="cat-thumbs">{thumbs}</span>
  <span class="cat-count">{len(items)} {"item" if len(items) == 1 else "items"}</span>
</a></li>"""
    bsets = next(p for p in PRODUCTS if p["slug"] == "build-set")
    builds = "".join(f"""<a class="build" href="products/build-set?edition={val['label'].lower()}">
  <div class="build-img"><img src="{img(val['img'], r, True)}" alt="{E(val['label'])} build set" loading="lazy"></div>
  <h3>{E(val['label'])}</h3><p>{E(val['note'])}, {fmt(val['price'])}</p></a>""" for val in bsets["values"])

    body = f"""<main id="main">
<section class="hero">
  <h1 class="hero-title">Made to be<br>picked up.</h1>
  <div class="hero-row">
    <p class="hero-copy">{E(STORE['description'])} Season one, in small runs.</p>
    <a class="btn btn-solid" href="shop">Shop the collection</a>
  </div>
  <figure class="hero-img"><img src="{img('ed-hero')}" alt="Someone in an ember hoodie and black cap sitting in a sunlit studio, holding a black mug" width="1536" height="864"></figure>
</section>

<section class="cats" aria-labelledby="cats-title">
  <h2 id="cats-title" class="section-title">Browse by what you'll do with it</h2>
  <ul class="cat-list">{cats}</ul>
</section>

<section class="grid-section" aria-labelledby="new-title">
  <div class="section-head"><h2 id="new-title" class="section-title">This season</h2><a href="shop" class="text-link">See all {len(PRODUCTS)} pieces</a></div>
  <div class="grid">{''.join(card(p, r, i) for i, p in enumerate(feat))}</div>
</section>

<section class="split">
  <figure class="split-img"><img src="{img('ed-desk')}" alt="A wooden desk with a felt desk mat, laptop sleeve, brick campfire build, ember bottle and lit candle" loading="lazy"></figure>
  <div class="split-copy">
    <h2>The desk, kept simple</h2>
    <p>A felt mat that quiets the keyboard, a pen with real weight to it, and a notebook that opens flat on the first page and the last.</p>
    <a class="btn btn-line" href="shop?c=desk">Shop desk</a>
  </div>
</section>

<section class="builds" aria-labelledby="builds-title">
  <div class="builds-copy">
    <h2 id="builds-title" class="section-title">Two build sets, designed in house</h2>
    <p>A small campfire for a quiet afternoon, or a two-storey studio with a sign that lights up. Both come with a printed booklet.</p>
  </div>
  <div class="builds-grid">{builds}</div>
</section>

<section class="pair">
  <figure><img src="{img('ed-wear')}" alt="Close crop of a bone hoodie and a canvas tote against a sunlit wall" loading="lazy"><figcaption><a href="shop?c=wear">Wear</a> Heavyweight, a little boxy.</figcaption></figure>
  <figure><img src="{img('ed-home')}" alt="Two lit candles beside a black mug and an ember beanie" loading="lazy"><figcaption><a href="shop?c=home">Home</a> For the end of the day.</figcaption></figure>
</section>

<section class="signup">
  <h2>Hear about the next drop</h2>
  <p>One email per season. No countdowns.</p>
  <form class="signup-form" data-demo-form>
    <label class="sr-only" for="email">Email address</label>
    <input id="email" type="email" placeholder="you@example.com" required autocomplete="email">
    <button class="btn btn-solid" type="submit">Sign up</button>
  </form>
</section>
</main>"""
    title = f"{STORE['name']} | {STORE['tagline']}"
    ld = {"@context": "https://schema.org", "@type": "Store", "name": STORE["name"], "description": STORE["description"], "url": abs_url("")}
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    return head(title, STORE["description"], r, abs_img("ed-hero"), extra) + header(r) + body + footer(r)


def page_shop():
    r = ""
    chips = '<button type="button" class="chip" data-filter="all" aria-pressed="true">Everything</button>' + "".join(
        f'<button type="button" class="chip" data-filter="{k}" aria-pressed="false">{name}</button>' for k, name, _ in CATEGORIES)
    blurbs = json.dumps({k: {"name": n, "blurb": b} for k, n, b in CATEGORIES})
    body = f"""<main id="main" class="shop">
  <div class="shop-head">
    <h1 class="shop-title" data-shop-title>Everything</h1>
    <p class="shop-blurb" data-shop-blurb>All {len(PRODUCTS)} pieces from season one.</p>
  </div>
  <div class="toolbar">
    <div class="chips" role="group" aria-label="Filter by category">{chips}</div>
    <label class="sort">Sort <select data-sort>
      <option value="featured">Featured</option>
      <option value="low">Price, low to high</option>
      <option value="high">Price, high to low</option>
    </select></label>
  </div>
  <p class="result-count" data-count aria-live="polite">{len(PRODUCTS)} pieces</p>
  <div class="grid" data-grid>{''.join(card(p, r, i) for i, p in enumerate(PRODUCTS))}</div>
  <script type="application/json" id="cat-data">{blurbs}</script>
</main>"""
    ld = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": abs_url(f"products/{p['slug']}"), "name": p["name"]} for i, p in enumerate(PRODUCTS)]}
    extra = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    return head(f"Shop | {STORE['name']}", STORE["description"], r, abs_img("ed-flatlay"), extra) + header(r, "all") + body + footer(r)


def page_product(p):
    r = "../"
    cat_name, _ = CAT[p["category"]]
    first = p["values"][0]
    opt = p["option"]
    swatch_html = ""
    if len(p["values"]) > 1:
        btns = "".join(
            f'<button type="button" class="swatch" data-value="{E(val["label"])}" aria-pressed="{"true" if i == 0 else "false"}" style="--c:{val["hex"]}"><span class="swatch-dot"></span><span>{E(val["label"])}</span>{f"<small>{E(val["note"])}</small>" if val.get("note") else ""}</button>'
            for i, val in enumerate(p["values"]))
        swatch_html = f'<fieldset class="opt"><legend>{opt}: <span data-opt-label>{E(first["label"])}</span></legend><div class="swatches">{btns}</div></fieldset>'
    else:
        swatch_html = f'<p class="opt-static">{opt}: {E(first["label"])}</p>'
    size_html = ""
    sizes = p.get("sizes")
    if sizes and sizes != ["One size"]:
        sbtn = "".join(f'<button type="button" class="size" data-size="{s}" aria-pressed="false">{s}</button>' for s in sizes)
        size_html = f'<fieldset class="opt"><legend>Size: <span data-size-label>Choose a size</span></legend><div class="sizes">{sbtn}</div><p class="fineprint">Boxy fit. Size down for a closer cut.</p></fieldset>'
    elif sizes:
        size_html = '<p class="opt-static">Size: One size</p>'

    gallery = [first["img"]] + EDITORIAL[p["category"]]
    gal = "".join(
        f'<figure class="gal-item"><img src="{img(k, r)}" alt="{E(p["name"]) if i == 0 else "Editorial photo"}" {"data-main-img" if i == 0 else "loading=\"lazy\""} width="896" height="1120"></figure>'
        for i, k in enumerate(gallery))

    details = "".join(f"<li>{E(d)}</li>" for d in p["details"])
    related = [q for q in PRODUCTS if q["category"] == p["category"] and q["slug"] != p["slug"]]
    if len(related) < 4:
        related += [q for q in PRODUCTS if q["category"] != p["category"]][: 4 - len(related)]
    rel_html = "".join(card(q, r, i) for i, q in enumerate(related[:4]))

    data = {
        "slug": p["slug"], "name": p["name"], "option": opt, "price": p["price"],
        "needsSize": bool(sizes and sizes != ["One size"]),
        "values": [{"label": val["label"], "img": img(val["img"], r), "price": val.get("price", p["price"]), "note": val.get("note")} for val in p["values"]],
        "variants": variants(p),
    }
    lo, hi = price_range(p)
    ld = {
        "@context": "https://schema.org", "@type": "ProductGroup",
        "name": p["name"], "description": p["summary"], "productGroupID": f"FLT-{p['sku']}",
        "brand": {"@type": "Brand", "name": STORE["name"]}, "category": cat_name,
        "url": abs_url(f"products/{p['slug']}"), "image": [abs_img(val["img"]) for val in p["values"]],
        "variesBy": (["https://schema.org/color"] if opt in ("Color", "Finish") else []) + (["https://schema.org/size"] if sizes else []),
        "offers": {"@type": "AggregateOffer", "priceCurrency": "USD", "lowPrice": lo, "highPrice": hi, "offerCount": len(data["variants"])},
        "hasVariant": [{
            "@type": "Product", "sku": vv["sku"], "name": " / ".join([p["name"]] + [str(vv[k]) for k in vv if k in (opt.lower(), "size")]),
            "image": vv["image"],
            **({"color": vv[opt.lower()]} if opt in ("Color", "Finish") else {}),
            **({"size": vv["size"]} if "size" in vv else {}),
            "offers": {"@type": "Offer", "price": vv["price"], "priceCurrency": "USD", "availability": "https://schema.org/InStock", "url": abs_url(f"products/{p['slug']}")},
        } for vv in data["variants"]],
    }
    extra = (f'<meta property="og:type" content="product"><meta property="product:price:amount" content="{lo}"><meta property="product:price:currency" content="USD">'
             f'<link rel="canonical" href="{abs_url("products/" + p["slug"])}">'
             f'<script type="application/ld+json">{json.dumps(ld)}</script>')
    badge = f'<span class="badge badge-inline">{E(p["badge"])}</span>' if p.get("badge") else ""
    body = f"""<main id="main" class="pdp" data-product-id="{p['slug']}">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="{r}shop">Shop</a><span aria-hidden="true">/</span><a href="{r}shop?c={p['category']}">{cat_name}</a></nav>
  <div class="pdp-layout">
    <div class="gallery">{gal}</div>
    <div class="buy">
      <div class="buy-inner">
        {badge}
        <h1 class="pdp-title">{E(p['name'])}</h1>
        <p class="pdp-price" data-price>{fmt(first.get('price', p['price']))}</p>
        <p class="pdp-summary">{E(p['summary'])}</p>
        {swatch_html}
        {size_html}
        <div class="qty-row">
          <div class="qty" aria-label="Quantity"><button type="button" data-qty="-1" aria-label="Decrease quantity">&minus;</button><output data-qty-value>1</output><button type="button" data-qty="1" aria-label="Increase quantity">+</button></div>
          <button type="button" class="btn btn-solid btn-grow" data-add>Add to bag</button>
        </div>
        <p class="hint" data-hint></p>
        <p class="sku">SKU <span data-sku>{data['variants'][0]['sku'] if not data['needsSize'] else 'select options'}</span></p>
        <details open><summary>Details</summary><ul class="detail-list">{details}</ul></details>
        <details><summary>Materials and care</summary><p>{E(p['materials'])}</p><p>{E(p['care'])}</p></details>
        <details><summary>Shipping and returns</summary><p>Ships in 2 to 4 working days. Returns are free within 30 days. (This is a demo storefront, so nothing will actually ship.)</p></details>
      </div>
    </div>
  </div>
  <section class="grid-section related" aria-labelledby="rel-title">
    <h2 id="rel-title" class="section-title">Goes well with</h2>
    <div class="grid">{rel_html}</div>
  </section>
  <script type="application/json" id="product-data">{json.dumps(data)}</script>
</main>"""
    return head(f"{p['name']} | {STORE['name']}", p["summary"], r, abs_img(first["img"]), extra) + header(r, p["category"]) + body + footer(r)


# ---------------------------------------------------------------- data exports
def export_json():
    out = {"store": STORE, "generated": date.today().isoformat(), "categories": [{"id": k, "name": n, "description": b} for k, n, b in CATEGORIES], "products": []}
    for p in PRODUCTS:
        lo, hi = price_range(p)
        out["products"].append({
            "id": p["slug"], "groupSku": f"FLT-{p['sku']}", "name": p["name"], "category": p["category"],
            "url": abs_url(f"products/{p['slug']}"), "summary": p["summary"], "details": p["details"],
            "materials": p["materials"], "care": p["care"], "badge": p.get("badge"),
            "priceMin": lo, "priceMax": hi, "currency": "USD",
            "options": [{"name": p["option"], "values": [{"label": val["label"], "hex": val["hex"], "image": abs_img(val["img"]), "thumbnail": img(val["img"], thumb=True) if not img(val["img"]).startswith("images/") else abs_url(img(val["img"], thumb=True)), **({"price": val["price"]} if "price" in val else {}), **({"note": val["note"]} if val.get("note") else {})} for val in p["values"]]}]
                       + ([{"name": "Size", "values": p["sizes"]}] if p.get("sizes") else []),
            "variants": variants(p),
        })
    return json.dumps(out, indent=2)


def export_feed():
    items = []
    for p in PRODUCTS:
        for vv in variants(p):
            attrs = [vv.get(p["option"].lower(), ""), vv.get("size", "")]
            title = p["name"] + "".join(f" - {a}" for a in attrs if a and a != "One size")
            items.append(f"""  <item>
    <g:id>{vv['sku']}</g:id>
    <g:item_group_id>FLT-{p['sku']}</g:item_group_id>
    <title>{E(title)}</title>
    <description>{E(p['summary'])}</description>
    <link>{E(abs_url('products/' + p['slug']))}</link>
    <g:image_link>{E(vv['image'])}</g:image_link>
    <g:price>{vv['price']:.2f} USD</g:price>
    <g:availability>in_stock</g:availability>
    <g:condition>new</g:condition>
    <g:brand>{STORE['name']}</g:brand>
    <g:product_type>{CAT[p['category']][0]}</g:product_type>{f"{chr(10)}    <g:color>{E(vv[p['option'].lower()])}</g:color>" if p['option'] in ('Color', 'Finish') else ''}{f"{chr(10)}    <g:size>{vv['size']}</g:size>" if vv.get('size') else ''}
  </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">
<channel>
  <title>{STORE['name']} product feed</title>
  <link>{E(abs_url(''))}</link>
  <description>{E(STORE['description'])}</description>
{chr(10).join(items)}
</channel>
</rss>
"""


def export_sitemap():
    urls = ["", "shop"] + [f"products/{p['slug']}" for p in PRODUCTS]
    body = "".join(f"  <url><loc>{E(abs_url(u))}</loc></url>\n" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}</urlset>\n'


def main():
    (ROOT / "products").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(page_home())
    (ROOT / "shop").write_text(page_shop())
    for p in PRODUCTS:
        (ROOT / "products" / f"{p['slug']}").write_text(page_product(p))
    (ROOT / "products.json").write_text(export_json())
    (ROOT / "feed.xml").write_text(export_feed())
    (ROOT / "sitemap.xml").write_text(export_sitemap())
    print(f"Built {len(PRODUCTS)} product pages, {sum(len(variants(p)) for p in PRODUCTS)} variants.")


if __name__ == "__main__":
    main()
