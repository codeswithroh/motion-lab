// Shared, deterministic helpers for the Whop spec ad.
(function () {
  const GLYPHS = "abcdefghijklmnopqrstuvwxyz$%#!?ABCDEFGHJKLMNPQRSTUVWXYZ";
  function hash(a, b, c) {
    let h = (a * 374761393 + b * 668265263 + c * 2147483647) | 0;
    h = Math.imul(h ^ (h >>> 13), 1274126177);
    return ((h ^ (h >>> 16)) >>> 0) / 4294967295;
  }
  // Types `text` into the element's .live span between characters fromN..toN,
  // with `scramble` random glyphs riding ahead of the cursor.
  function type(tl, root, sel, text, at, dur, opts) {
    const o = Object.assign({ from: 0, to: text.length, scramble: 3, seed: 1 }, opts || {});
    const el = root.querySelector(sel + " .live");
    const proxy = { p: 0 };
    tl.fromTo(
      proxy,
      { p: 0 },
      {
        p: 1,
        duration: dur,
        ease: "none",
        immediateRender: false,
        onUpdate: function () {
          const p = proxy.p;
          const n = Math.round(o.from + (o.to - o.from) * p);
          let s = text.slice(0, n);
          if (p < 1) {
            const step = Math.floor(p * dur * 30);
            for (let i = 0; i < o.scramble && n + i < o.to; i++) {
              if (text[n + i] === " ") { s += " "; continue; }
              s += GLYPHS[Math.floor(hash(step, i, o.seed) * GLYPHS.length)];
            }
          }
          el.textContent = s;
        },
      },
      at,
    );
  }
  // Pill pop-in: quick horizontal stretch from the left edge.
  function pop(tl, root, sel, at) {
    tl.fromTo(
      root.querySelector(sel),
      { opacity: 0, scaleX: 0.55, transformOrigin: "0% 50%" },
      { opacity: 1, scaleX: 1, duration: 0.14, ease: "power3.out" },
      at,
    );
  }
  window.fx = { type, pop, hash };
})();
