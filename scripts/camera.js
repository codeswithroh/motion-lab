// Beat-driven camera for a HyperFrames root composition. Copy to assets/camera.js and load it
// after gsap and assets/cues.js (written by score.py). Proven on the Whop spec ad.
//
//   <div id="dim-host" class="clip" data-start="0" data-duration="<film>" data-layout-ignore
//        style="position:absolute;inset:0;z-index:800;pointer-events:none"><div id="dim"></div></div>
//   <div id="flash-host" ... z-index:850 ...><div id="flash"></div></div>
//   #dim  { position:absolute; inset:0; background:#000; opacity:0 }
//   #flash{ position:absolute; inset:0; background:#fff; opacity:0 }
//
//   motionCamera(tl, {
//     scenes: [["hook", 0, 2.6667], ["proof", 2.6667, 8], ...],   // [host id, start, duration]
//     cues: window.CUES,
//     shake: [[0, 5.3333], [20.6667, 99]],   // intro + outro only. The person rejected shake in the middle.
//   });
//
// Amounts are the ones the person approved after "the screen is shaking a lot":
// kick 2.2% push, clap 0.3 deg + 4 px, roll 2 px, cut whip 70 px, hit 10% punch + white flash.
// Drop-outs darken (55%) and creep in 10% while the music holds its breath, then flash on the hit.
// Flash and dim are not shake: they stay on in the middle.
(function () {
  function motionCamera(tl, o) {
    const S = o.scenes, C = o.cues, k = o.strength || 1, IR = { immediateRender: false };
    const zones = o.shake || [[0, 1e9]];
    const shake = (t) => zones.some(([a, b]) => t >= a - 1e-3 && t < b - 1e-3);
    const host = (t) => { for (const [id, s, d] of S) if (t >= s - 1e-3 && t < s + d - 1e-3) return "#" + id; return null; };
    S.forEach(([id]) => gsap.set("#" + id, { transformOrigin: "50% 50%" }));
    const on = (list, fn) => (list || []).forEach((t, i) => { const h = host(t); if (h && shake(t)) fn(h, t, i); });
    on(C.kick, (h, t) => tl.fromTo(h, { scale: 1 + 0.022 * k }, { scale: 1, duration: 0.24, ease: "power3.out", ...IR }, t));
    on(C.clap, (h, t, i) => tl.fromTo(h, { rotation: (i % 2 ? 0.3 : -0.3) * k, y: -4 * k, scale: 1 + 0.03 * k },
      { rotation: 0, y: 0, scale: 1, duration: 0.22, ease: "power2.out", ...IR }, t));
    on(C.roll, (h, t, i) => tl.fromTo(h, { y: (i % 2 ? 2 : -2) * k, scale: 1 + 0.008 * k }, { y: 0, scale: 1, duration: 0.07, ease: "none", ...IR }, t));
    S.forEach(([id, s], i) => { if (s > 0 && shake(s)) tl.fromTo("#" + id, { x: (i % 2 ? 70 : -70) * k, scale: 1 + 0.06 * k }, { x: 0, scale: 1, duration: 0.18, ease: "power3.out", ...IR }, s); });
    (C.drops || []).forEach(([a, b]) => {
      tl.fromTo("#dim", { opacity: 0 }, { opacity: 0.55, duration: b - a, ease: "power2.in", ...IR }, a);
      tl.fromTo("#dim", { opacity: 0.55 }, { opacity: 0, duration: 0.05, ...IR }, b);
      const h = host(a);
      if (h && shake(a)) tl.fromTo(h, { scale: 1 }, { scale: 1 + 0.1 * k, duration: b - a, ease: "power2.in", ...IR }, a);
    });
    (C.hits || []).forEach((t) => {
      tl.fromTo("#flash", { opacity: 0.85 }, { opacity: 0, duration: 0.32, ease: "power2.out", ...IR }, t);
      const h = host(t);
      if (h && shake(t)) tl.fromTo(h, { scale: 1 + 0.1 * k, x: 0, rotation: 0 }, { scale: 1, duration: 0.5, ease: "expo.out", ...IR }, t);
    });
  }
  window.motionCamera = motionCamera;
})();
