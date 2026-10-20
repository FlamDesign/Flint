# Flint demo storefront

A static, curated merch store used as a live page example. Nothing is for sale:
the bag works, checkout is turned off.

17 products, 70 variants (color, finish, edition or scent, plus sizes on apparel),
and 40 studio and editorial photographs.

## Structure

```
index.html            Home
shop.html             All products, filter by category (?c=wear|carry|desk|home|play), sort
products/<slug>.html  One static page per product (variant via ?color=ink, ?edition=studio, etc.)
products.json         Full catalog with every variant, SKU, price and image URL
feed.xml              Google Merchant style RSS feed, one item per variant
sitemap.xml
assets/               styles.css, app.js, favicon.svg
catalog.py            Source of truth for products
build.py              Generates every page and data file from catalog.py
images.tsv            Image key to hosted URL map
```

## Data available on every product page

- `application/ld+json` ProductGroup with `hasVariant` (sku, color/size, image, price, availability)
- Open Graph tags (`og:title`, `og:image`, `product:price:amount`)
- `data-product-id` on the page root and on every product card, with schema.org microdata on cards
- A `#product-data` JSON block with the same variant data the page uses

## Publish on GitHub Pages

Deployment is automatic. In the repo, set Settings > Pages > Source to **GitHub Actions**.
Every push to `main` then runs `.github/workflows/pages.yml`, which copies the product
images into the site, rebuilds with absolute URLs, and deploys.

## Editing

Change `catalog.py`, run `python3 build.py`, commit. Python 3.12+.
