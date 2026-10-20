/* Flint demo storefront: bag, filters, variant picker. No checkout. */
(() => {
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const money = n => "$" + Number(n).toLocaleString("en-US", { maximumFractionDigits: 0 });
  const cartEl = $("#cart");
  const ROOT = cartEl ? cartEl.dataset.root : "";
  const KEY = "flint-bag-v1";
  const withRoot = p => (/^https?:/.test(p) ? p : ROOT + p);

  /* ---------- storage (safe in private mode) */
  let memory = [];
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || []; } catch { return memory; } };
  const save = lines => { memory = lines; try { localStorage.setItem(KEY, JSON.stringify(lines)); } catch {} };

  /* ---------- toast */
  const toastEl = $("[data-toast]");
  let toastTimer;
  const toast = msg => {
    if (!toastEl) return;
    toastEl.textContent = msg;
    toastEl.classList.add("is-visible");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove("is-visible"), 2600);
  };

  /* ---------- bag */
  const render = () => {
    const lines = load();
    const count = lines.reduce((a, l) => a + l.qty, 0);
    $$("[data-cart-count]").forEach(el => { el.textContent = count; el.classList.toggle("has-items", count > 0); });
    const list = $("[data-cart-lines]");
    if (!list) return;
    $("[data-cart-empty]").hidden = lines.length > 0;
    $("[data-cart-foot]").hidden = lines.length === 0;
    $("[data-cart-subtotal]").textContent = money(lines.reduce((a, l) => a + l.qty * l.price, 0));
    list.innerHTML = lines.map((l, i) => `
      <li class="cart-line">
        <a href="${withRoot(l.url)}"><img src="${withRoot(l.img)}" alt=""></a>
        <div>
          <h3>${l.name}</h3>
          <p>${[l.option, l.size].filter(Boolean).join(", ")}</p>
          <div class="cart-line-actions">
            <div class="qty" aria-label="Quantity"><button type="button" data-line="${i}" data-step="-1" aria-label="Decrease">&minus;</button><output>${l.qty}</output><button type="button" data-line="${i}" data-step="1" aria-label="Increase">+</button></div>
            <button type="button" class="link-btn" data-remove="${i}">Remove</button>
          </div>
        </div>
        <span class="cart-line-price">${money(l.price * l.qty)}</span>
      </li>`).join("");
  };

  const openCart = () => { cartEl.classList.add("is-open"); cartEl.setAttribute("aria-hidden", "false"); $(".cart-panel button", cartEl)?.focus(); };
  const closeCart = () => { cartEl.classList.remove("is-open"); cartEl.setAttribute("aria-hidden", "true"); };

  document.addEventListener("click", e => {
    const t = e.target.closest("button, a");
    if (!t) return;
    if (t.matches("[data-open-cart]")) openCart();
    else if (t.matches("[data-close-cart]")) closeCart();
    else if (t.matches("[data-checkout]")) toast("Checkout is turned off on this demo storefront.");
    else if (t.dataset.step) {
      const lines = load(); const l = lines[+t.dataset.line];
      l.qty = Math.max(0, l.qty + +t.dataset.step);
      save(lines.filter(x => x.qty > 0)); render();
    } else if (t.dataset.remove !== undefined) {
      const lines = load(); lines.splice(+t.dataset.remove, 1); save(lines); render();
    }
  });
  $(".cart-scrim")?.addEventListener("click", closeCart);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && cartEl?.classList.contains("is-open")) closeCart(); });

  $$("[data-demo-form]").forEach(f => f.addEventListener("submit", e => {
    e.preventDefault(); f.reset(); toast("Signed up. (Demo only, no email will be sent.)");
  }));

  /* ---------- shop: filter + sort */
  const grid = $("[data-grid]");
  if (grid) {
    const cats = JSON.parse($("#cat-data").textContent);
    const cards = $$(".card", grid);
    const title = $("[data-shop-title]"), blurb = $("[data-shop-blurb]"), count = $("[data-count]");
    const sortSel = $("[data-sort]");
    const apply = (filter, push) => {
      $$("[data-filter]").forEach(c => c.setAttribute("aria-pressed", String(c.dataset.filter === filter)));
      let n = 0;
      cards.forEach(c => { const show = filter === "all" || c.dataset.category === filter; c.hidden = !show; n += show; });
      title.textContent = filter === "all" ? "Everything" : cats[filter].name;
      blurb.textContent = filter === "all" ? `All ${cards.length} pieces from season one.` : cats[filter].blurb;
      count.textContent = `${n} ${n === 1 ? "piece" : "pieces"}`;
      $$(".nav-cats a").forEach(a => a.toggleAttribute("aria-current", a.href.endsWith("c=" + filter)));
      if (push) history.replaceState(null, "", filter === "all" ? "shop" : `shop?c=${filter}`);
    };
    const sort = mode => {
      const by = { featured: (a, b) => a.dataset.order - b.dataset.order, low: (a, b) => a.dataset.price - b.dataset.price, high: (a, b) => b.dataset.price - a.dataset.price }[mode];
      cards.slice().sort(by).forEach(c => grid.appendChild(c));
    };
    $$("[data-filter]").forEach(c => c.addEventListener("click", () => apply(c.dataset.filter, true)));
    sortSel.addEventListener("change", () => sort(sortSel.value));
    const initial = new URLSearchParams(location.search).get("c");
    apply(cats[initial] ? initial : "all", false);
  }

  /* ---------- product page */
  const dataEl = $("#product-data");
  if (dataEl) {
    const P = JSON.parse(dataEl.textContent);
    const optKey = P.option.toLowerCase();
    const params = new URLSearchParams(location.search);
    const fromUrl = (params.get(optKey) || "").toLowerCase();
    let value = P.values.find(v => v.label.toLowerCase() === fromUrl) || P.values[0];
    let size = null, qty = 1;
    const mainImg = $("[data-main-img]");

    const variant = () => P.variants.find(v => v[optKey] === value.label && (!P.needsSize || v.size === size));
    const sync = (instant) => {
      $$(".swatch").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.value === value.label)));
      const lbl = $("[data-opt-label]"); if (lbl) lbl.textContent = value.label;
      $("[data-price]").textContent = money(value.price);
      if (mainImg && !mainImg.src.endsWith(value.img.replace(/^\.\.\//, ""))) {
        if (instant) { mainImg.src = value.img; mainImg.alt = `${P.name} in ${value.label}`; }
        else {
        mainImg.classList.add("is-swapping");
        const pre = new Image();
        pre.onload = () => { mainImg.src = value.img; mainImg.alt = `${P.name} in ${value.label}`; mainImg.classList.remove("is-swapping"); };
        pre.src = value.img;
        }
      }
      const v = variant();
      $("[data-sku]").textContent = v ? v.sku : "select a size";
      $("[data-main]")?.setAttribute("data-sku", v ? v.sku : "");
    };

    $$(".swatch").forEach(b => b.addEventListener("click", () => {
      value = P.values.find(v => v.label === b.dataset.value);
      const u = new URL(location.href); u.searchParams.set(optKey, value.label.toLowerCase()); history.replaceState(null, "", u);
      sync();
    }));
    $$(".size").forEach(b => b.addEventListener("click", () => {
      size = b.dataset.size;
      $$(".size").forEach(x => x.setAttribute("aria-pressed", String(x === b)));
      $("[data-size-label]").textContent = size;
      $("[data-hint]").textContent = "";
      sync();
    }));
    $$("[data-qty]").forEach(b => b.addEventListener("click", () => {
      qty = Math.min(9, Math.max(1, qty + +b.dataset.qty));
      $("[data-qty-value]").textContent = qty;
    }));
    $("[data-add]").addEventListener("click", () => {
      if (P.needsSize && !size) { $("[data-hint]").textContent = "Choose a size to add this to your bag."; $(".size")?.focus(); return; }
      const v = variant();
      const lines = load();
      const existing = lines.find(l => l.sku === v.sku);
      if (existing) existing.qty += qty;
      else lines.push({
        sku: v.sku, name: P.name, option: P.values.length > 1 ? value.label : "", size: size || "",
        price: value.price, qty, img: value.img.replace(/^\.\.\//, ""), url: `products/${P.slug}`,
      });
      save(lines); render(); openCart();
    });
    sync(true);
  }

  render();
})();
