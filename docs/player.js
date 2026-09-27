/* Reading-edition behavior: chapter rail fixes, scrollable tables, and the
   narration player. The player only appears once a real audio file has
   answered, so a copy of this page without site/audio shows no dead buttons. */
(function () {
  "use strict";

  // The rail joins "Chapter N." and the title with a line break; show a space.
  document.querySelectorAll(".rail br").forEach(function (b) { b.replaceWith(" "); });

  // Wide tables scroll inside the column, reachable by keyboard.
  document.querySelectorAll("main table").forEach(function (table) {
    var wrap = document.createElement("div");
    wrap.className = "table-scroll";
    wrap.tabIndex = 0;
    wrap.setAttribute("role", "region");
    wrap.setAttribute("aria-label", "Scrollable table");
    table.before(wrap);
    wrap.append(table);
  });

  if (typeof AUDIO === "undefined" || !AUDIO || !AUDIO.tracks) return;
  var order = Object.keys(AUDIO.tracks).filter(function (id) { return AUDIO.tracks[id].sec; });
  if (!order.length) return;

  var RATES = [1, 1.25, 1.5, 0.9];
  var store = {
    get: function (k, d) { try { return localStorage.getItem(k) || d; } catch (e) { return d; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };
  function $(sel) { return document.querySelector(sel); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function clock(s) {
    if (!isFinite(s) || s < 0) s = 0;
    var m = Math.floor(s / 60), r = Math.round(s % 60);
    if (r === 60) { m += 1; r = 0; }
    return m + ":" + (r < 10 ? "0" : "") + r;
  }
  function title(id) { return AUDIO.tracks[id].t; }

  var el = new Audio();
  el.preload = "metadata";
  var rate = parseFloat(store.get("dm-narration-rate", "1")) || 1;
  var continuous = false;
  var active = null;
  var strips = {};
  function rateLabel() { return (rate % 1 === 0 ? rate.toFixed(1) : String(rate)) + "×"; }

  order.forEach(function (id) {
    var sec = document.getElementById(AUDIO.tracks[id].sec);
    if (!sec) return;
    var strip = document.createElement("div");
    strip.className = "aud";
    strip.setAttribute("data-ch", id);
    strip.innerHTML =
      '<button class="aud-play" type="button" aria-label="Play narration for ' + esc(title(id)) + '">&#9654;</button>' +
      '<span class="aud-lbl">Listen</span>' +
      '<input class="aud-seek" type="range" min="0" max="1000" value="0" step="1" aria-label="Seek within narration">' +
      '<span class="aud-time"><b>0:00</b> / ' + clock(AUDIO.tracks[id].d) + "</span>" +
      '<button class="aud-rate" type="button" aria-label="Playback speed">' + rateLabel() + "</button>";
    var h = sec.querySelector("h1");
    if (h && h.parentNode === sec) sec.insertBefore(strip, h.nextSibling);
    else sec.insertBefore(strip, sec.firstChild);
    strips[id] = strip;
  });

  var bar = document.createElement("div");
  bar.className = "aud-bar";
  bar.innerHTML =
    '<span class="t">Now playing · <b></b></span>' +
    '<button data-a="prev" type="button" aria-label="Previous section">&#8592;</button>' +
    '<button data-a="toggle" type="button" aria-label="Pause">&#10073;&#10073;</button>' +
    '<button data-a="next" type="button" aria-label="Next section">&#8594;</button>' +
    '<button data-a="cont" type="button" aria-pressed="false">Continuous</button>' +
    '<button data-a="stop" type="button" aria-label="Stop narration">&#10005;</button>';
  document.body.appendChild(bar);
  var barTitle = bar.querySelector(".t b");
  var barToggle = bar.querySelector('[data-a="toggle"]');
  var barCont = bar.querySelector('[data-a="cont"]');

  var pendingSeek = null;
  function seekTo(t) { if (el.readyState > 0) { el.currentTime = t; pendingSeek = null; } else pendingSeek = t; }
  function load(id) {
    if (active === id) return;
    active = id;
    pendingSeek = null;
    el.src = AUDIO.dir + AUDIO.tracks[id].f;
    el.playbackRate = rate;
    barTitle.textContent = title(id);
  }
  function play(id, at) {
    load(id);
    if (typeof at === "number") seekTo(at);
    var p = el.play();
    if (p && p.catch) p.catch(function () { paint(); });
  }
  function step(delta, scroll) {
    var i = order.indexOf(active) + delta;
    if (i < 0 || i >= order.length) return false;
    var id = order[i];
    play(id, 0);
    if (scroll) {
      var sec = document.getElementById(AUDIO.tracks[id].sec);
      if (sec) sec.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    return true;
  }

  function set(node, prop, value) { if (node[prop] !== value) node[prop] = value; }
  function paintStrip(id, playing) {
    var s = strips[id];
    if (!s) return;
    var isActive = id === active, on = isActive && playing;
    var dur = (isActive && isFinite(el.duration) && el.duration) || AUDIO.tracks[id].d;
    var at = isActive ? el.currentTime : 0;
    s.classList.toggle("on", on);
    var btn = s.querySelector(".aud-play");
    set(btn, "innerHTML", on ? "&#10073;&#10073;" : "&#9654;");
    btn.setAttribute("aria-label", (on ? "Pause narration for " : "Play narration for ") + title(id));
    set(s.querySelector(".aud-lbl"), "textContent", on ? "Playing" : "Listen");
    set(s.querySelector(".aud-seek"), "value", String(Math.round((at / dur) * 1000) || 0));
    set(s.querySelector(".aud-time"), "innerHTML", "<b>" + clock(at) + "</b> / " + clock(dur));
    set(s.querySelector(".aud-rate"), "innerHTML", rateLabel());
  }
  function paint() {
    var playing = !el.paused && !el.ended;
    order.forEach(function (id) { paintStrip(id, playing); });
    set(barToggle, "innerHTML", playing ? "&#10073;&#10073;" : "&#9654;");
    barToggle.setAttribute("aria-label", playing ? "Pause" : "Play");
    bar.classList.toggle("up", !!active && (playing || el.currentTime > 0));
  }

  el.addEventListener("timeupdate", paint);
  el.addEventListener("play", paint);
  el.addEventListener("pause", paint);
  el.addEventListener("loadedmetadata", function () {
    if (pendingSeek !== null) { el.currentTime = pendingSeek; pendingSeek = null; }
    paint();
  });
  el.addEventListener("ended", function () { if (continuous && step(1, true)) return; paint(); });
  el.addEventListener("error", function () { bar.classList.remove("up"); });

  document.addEventListener("click", function (e) {
    var strip = e.target.closest ? e.target.closest(".aud") : null;
    if (!strip) return;
    var id = strip.getAttribute("data-ch");
    if (e.target.closest(".aud-play")) {
      if (id === active && !el.paused) el.pause(); else play(id);
    } else if (e.target.closest(".aud-rate")) {
      rate = RATES[(RATES.indexOf(rate) + 1) % RATES.length];
      el.playbackRate = rate;
      store.set("dm-narration-rate", String(rate));
      paint();
    }
  });
  document.addEventListener("input", function (e) {
    if (!e.target.classList || !e.target.classList.contains("aud-seek")) return;
    var id = e.target.closest(".aud").getAttribute("data-ch");
    var frac = e.target.value / 1000;
    if (id !== active) play(id, frac * AUDIO.tracks[id].d);
    else seekTo(frac * (isFinite(el.duration) ? el.duration : AUDIO.tracks[id].d));
  });
  bar.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    var a = b.getAttribute("data-a");
    if (a === "toggle") { if (el.paused) play(active || order[0]); else el.pause(); }
    else if (a === "next") step(1, true);
    else if (a === "prev") { if (el.currentTime > 3) seekTo(0); else step(-1, true); }
    else if (a === "cont") { continuous = !continuous; barCont.setAttribute("aria-pressed", String(continuous)); }
    else if (a === "stop") { el.pause(); el.currentTime = 0; active = null; bar.classList.remove("up"); paint(); }
  });

  var total = order.reduce(function (n, id) { return n + AUDIO.tracks[id].d; }, 0);
  var intro = $("#aud-intro");
  $("#aud-total").textContent = "about " + Math.round(total / 60) + " minutes";
  $("#aud-credit").textContent = (AUDIO.credit || "") + " · " + order.length + " sections";
  $("#aud-start").addEventListener("click", function () {
    continuous = true;
    barCont.setAttribute("aria-pressed", "true");
    play(order[0]);
  });

  /* Reveal the player only once a file has answered. Chrome stalls media in a
     background tab, so re-arm the probe whenever the tab becomes visible. */
  var settled = false;
  var probe = new Audio();
  probe.preload = "metadata";
  probe.addEventListener("loadedmetadata", function () {
    if (settled) return;
    settled = true;
    Object.keys(strips).forEach(function (id) { strips[id].style.display = ""; });
    intro.classList.add("ready");
    paint();
  });
  probe.addEventListener("error", function () {
    if (settled) return;
    settled = true;
    Object.keys(strips).forEach(function (id) { strips[id].remove(); });
    bar.remove();
  });
  function probeNow() {
    if (settled || document.hidden) return;
    probe.src = AUDIO.dir + AUDIO.tracks[order[0]].f;
    probe.load();
  }
  document.addEventListener("visibilitychange", probeNow);
  Object.keys(strips).forEach(function (id) { strips[id].style.display = "none"; });
  probeNow();
})();
