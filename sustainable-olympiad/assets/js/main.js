/* Sustainable Olympiad: shared site behaviour (no dependencies). */
(function () {
  "use strict";

  var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var root = document.documentElement;
  var CONFIG = window.SO_CONFIG || {};

  /* ------------------------------------------------------------------
     Accessibility preferences
  ------------------------------------------------------------------ */
  var STORE = "so-a11y";
  var FONT_STEPS = [90, 100, 112.5, 125, 150, 175, 200];

  function loadPrefs() {
    try { return JSON.parse(localStorage.getItem(STORE) || "{}") || {}; } catch (e) { return {}; }
  }
  function savePrefs(p) {
    try { localStorage.setItem(STORE, JSON.stringify(p)); } catch (e) { /* storage unavailable: preferences last for this page only */ }
  }
  var prefs = loadPrefs();

  function systemDark() {
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  }
  function isDark() {
    return prefs.theme ? prefs.theme === "dark" : systemDark();
  }

  function applyPrefs() {
    if (prefs.theme) root.setAttribute("data-theme", prefs.theme); else root.removeAttribute("data-theme");
    toggleAttr("data-contrast", prefs.contrast, "high");
    toggleAttr("data-spacing", prefs.spacing, "wide");
    toggleAttr("data-links", prefs.links, "highlight");
    var font = prefs.font || 100;
    root.style.fontSize = font === 100 ? "" : font + "%";
    var status = $("#a11y-font-status");
    if (status) status.textContent = "Text size " + Math.round(font) + "%";
    setPressed("dark", isDark());
    setPressed("contrast", !!prefs.contrast);
    setPressed("spacing", !!prefs.spacing);
    setPressed("links", !!prefs.links);
  }
  function toggleAttr(name, on, value) {
    if (on) root.setAttribute(name, value); else root.removeAttribute(name);
  }
  function setPressed(key, on) {
    var b = $('[data-a11y="' + key + '"]');
    if (b) b.setAttribute("aria-pressed", on ? "true" : "false");
  }

  function initA11yPanel() {
    var toggle = $(".a11y-toggle");
    var panel = $("#a11y-panel");
    if (!toggle || !panel) return;

    function setOpen(open, returnFocus) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      panel.hidden = !open;
      if (!open && returnFocus) toggle.focus();
    }
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    panel.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape") setOpen(false, true);
    });

    panel.addEventListener("click", function (ev) {
      var btn = ev.target.closest("[data-a11y]");
      if (!btn) return;
      var action = btn.getAttribute("data-a11y");
      var idx = FONT_STEPS.indexOf(prefs.font || 100);
      if (idx < 0) idx = 1;
      switch (action) {
        case "font-up": prefs.font = FONT_STEPS[Math.min(idx + 1, FONT_STEPS.length - 1)]; break;
        case "font-down": prefs.font = FONT_STEPS[Math.max(idx - 1, 0)]; break;
        case "font-reset": prefs.font = 100; break;
        case "dark": prefs.theme = isDark() ? "light" : "dark"; break;
        case "contrast": prefs.contrast = !prefs.contrast; break;
        case "spacing": prefs.spacing = !prefs.spacing; break;
        case "links": prefs.links = !prefs.links; break;
        case "reset": prefs = {}; break;
      }
      savePrefs(prefs);
      applyPrefs();
      fitNav();
      if (action === "reset") announce("Accessibility settings reset");
    });

    if (window.matchMedia) {
      var mq = window.matchMedia("(prefers-color-scheme: dark)");
      var onChange = function () { if (!prefs.theme) applyPrefs(); };
      if (mq.addEventListener) mq.addEventListener("change", onChange); else if (mq.addListener) mq.addListener(onChange);
    }
    applyPrefs();
  }

  /* Polite announcements for screen readers */
  var liveRegion;
  function announce(msg) {
    if (!liveRegion) {
      liveRegion = document.createElement("div");
      liveRegion.className = "visually-hidden";
      liveRegion.setAttribute("role", "status");
      liveRegion.setAttribute("aria-live", "polite");
      document.body.appendChild(liveRegion);
    }
    liveRegion.textContent = "";
    setTimeout(function () { liveRegion.textContent = msg; }, 50);
  }

  /* ------------------------------------------------------------------
     Mobile navigation
  ------------------------------------------------------------------ */
  function initNav() {
    var toggle = $(".nav-toggle");
    var nav = $("#primary-nav");
    if (!toggle || !nav) return;
    var label = $(".nav-toggle-label", toggle);

    function setOpen(open, returnFocus) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      nav.classList.toggle("is-open", open);
      if (label) label.textContent = open ? "Close" : "Menu";
      if (!open && returnFocus) toggle.focus();
    }
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    document.addEventListener("keydown", function (ev) {
      if (ev.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") setOpen(false, true);
    });
    // Close when focus or a click leaves the header
    document.addEventListener("click", function (ev) {
      if (toggle.getAttribute("aria-expanded") === "true" && !ev.target.closest(".site-header")) setOpen(false);
    });
    nav.addEventListener("focusout", function (ev) {
      if (toggle.getAttribute("aria-expanded") === "true" && ev.relatedTarget &&
          !ev.relatedTarget.closest(".site-header")) setOpen(false);
    });
    var inner = $(".header-inner");
    var brand = $(".brand", inner);
    function fit() {
      var wasCompact = root.classList.contains("nav-compact");
      root.classList.remove("nav-compact");
      var list = $("ul", nav);
      var needed = brand.offsetWidth + list.scrollWidth + 24;
      var compact = needed > inner.clientWidth;
      root.classList.toggle("nav-compact", compact);
      if (wasCompact && !compact) setOpen(false);
    }
    fitNav = fit;
    var t;
    window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(fit, 100); });
    fit();
  }
  var fitNav = function () {};

  /* Skip link / in-page anchors: move keyboard focus to the target */
  function initAnchors() {
    document.addEventListener("click", function (ev) {
      var a = ev.target.closest('a[href^="#"]');
      if (!a || a.getAttribute("href").length < 2) return;
      var target = document.getElementById(a.getAttribute("href").slice(1));
      if (!target) return;
      if (!target.hasAttribute("tabindex") && !/^(A|BUTTON|INPUT|SELECT|TEXTAREA)$/.test(target.tagName)) {
        target.setAttribute("tabindex", "-1");
      }
      setTimeout(function () { target.focus({ preventScroll: true }); }, 0);
    });
  }

  /* ------------------------------------------------------------------
     Countdown (WCAG 2.2.2: can be paused)
  ------------------------------------------------------------------ */
  function initCountdowns() {
    $$("[data-countdown]").forEach(function (grid) {
      var section = grid.closest(".countdown");
      var target = new Date(grid.getAttribute("data-countdown")).getTime();
      var toggle = $("[data-countdown-toggle]", section);
      var done = $(".cd-done", section);
      var nums = {};
      $$(".cd-num", grid).forEach(function (n) { nums[n.getAttribute("data-unit")] = n; });
      var timer = null;
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

      function pad(n) { return n < 10 ? "0" + n : String(n); }
      function tick() {
        var diff = Math.max(0, target - Date.now());
        var s = Math.floor(diff / 1000);
        nums.days.textContent = Math.floor(s / 86400);
        nums.hours.textContent = pad(Math.floor((s % 86400) / 3600));
        nums.minutes.textContent = pad(Math.floor((s % 3600) / 60));
        nums.seconds.textContent = pad(s % 60);
        if (diff === 0) {
          stop();
          grid.hidden = true;
          if (done) done.hidden = false;
          if (toggle) toggle.hidden = true;
        }
      }
      function start() { tick(); timer = setInterval(tick, 1000); }
      function stop() { clearInterval(timer); timer = null; }

      tick();
      if (toggle) {
        toggle.hidden = false;
        toggle.addEventListener("click", function () {
          if (timer) { stop(); toggle.textContent = "Resume countdown"; }
          else { start(); toggle.textContent = "Pause countdown"; }
        });
      }
      // Users who prefer reduced motion start with a paused (static) countdown
      if (reduce) { if (toggle) toggle.textContent = "Resume countdown"; }
      else start();
    });
  }

  /* ------------------------------------------------------------------
     Timeline / key-date status labels
  ------------------------------------------------------------------ */
  function initTimeline() {
    var today = new Date();
    var todayStr = today.getFullYear() + "-" + ("0" + (today.getMonth() + 1)).slice(-2) + "-" + ("0" + today.getDate()).slice(-2);
    var nextFound = false;
    $$("[data-start]").forEach(function (item) {
      var start = item.getAttribute("data-start");
      var end = item.getAttribute("data-end") || start;
      var status = $(".tl-status", item);
      var label = "";
      if (end < todayStr) { item.classList.add("is-past"); label = "Completed"; }
      else if (start <= todayStr) { item.classList.add("is-current"); label = "Happening now"; nextFound = true; }
      else if (!nextFound) { item.classList.add("is-current"); label = "Up next"; nextFound = true; }
      if (status) status.textContent = label;
    });
  }

  /* ------------------------------------------------------------------
     Forms: validation, error summary, submission
  ------------------------------------------------------------------ */
  function fieldLabel(el) {
    var l = el.id && document.querySelector('label[for="' + el.id + '"]');
    if (!l) return el.name;
    var clone = l.cloneNode(true);
    $$(".req, .opt, .visually-hidden", clone).forEach(function (n) { n.remove(); });
    return clone.textContent.replace(/\s+/g, " ").trim();
  }

  function validateField(el) {
    if (el.disabled || el.closest("[hidden]")) return "";
    var v = el.type === "checkbox" ? el.checked : (el.value || "").trim();
    if (el.required && !v) {
      return el.getAttribute("data-error-required") || "Enter " + fieldLabel(el).toLowerCase();
    }
    if (el.type === "email" && v && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v)) {
      return "Enter an email address in the correct format, like name@example.com";
    }
    var min = el.getAttribute("minlength");
    if (min && v && v.length < +min) {
      return el.getAttribute("data-error-minlength") || "Must be at least " + min + " characters";
    }
    var max = el.getAttribute("maxlength");
    if (max && v && v.length > +max) return "Must be " + max + " characters or fewer";
    return "";
  }

  function showError(el, msg) {
    var err = document.getElementById(el.id + "-error");
    if (msg) el.setAttribute("aria-invalid", "true"); else el.removeAttribute("aria-invalid");
    if (err) err.textContent = msg ? msg : "";
    if (err && msg) { var hidden = document.createElement("span"); hidden.className = "visually-hidden"; hidden.textContent = "Error: "; err.prepend(hidden); }
  }

  function serialize(form) {
    var lines = [];
    $$("input, select, textarea", form).forEach(function (el) {
      if (!el.name || el.type === "submit" || el.closest("[hidden]")) return;
      var val;
      if (el.type === "checkbox") val = el.checked ? "Yes" : "No";
      else if (el.tagName === "SELECT") val = el.value ? el.options[el.selectedIndex].text : "";
      else val = el.value.trim();
      if (val) lines.push(fieldLabel(el) + ": " + val);
    });
    return lines.join("\n");
  }

  function submitForm(form) {
    var subject = form.getAttribute("data-subject") || "Website form";
    if (CONFIG.formEndpoint) {
      var data = new FormData(form);
      data.append("_subject", subject);
      return fetch(CONFIG.formEndpoint, { method: "POST", body: data, headers: { Accept: "application/json" } })
        .then(function (r) { if (!r.ok) throw new Error("Request failed"); return "sent"; });
    }
    // No endpoint configured: hand the message to the visitor's email app
    var href = "mailto:" + encodeURIComponent(CONFIG.contactEmail || "") +
      "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(serialize(form));
    window.location.href = href;
    return Promise.resolve("mailto");
  }

  function initForms() {
    $$("form.so-form").forEach(function (form) {
      form.setAttribute("novalidate", "");
      var kind = form.getAttribute("data-form");
      var summary = document.getElementById(kind + "-errors");
      var success = document.getElementById(kind + "-success");
      var status = form.querySelector(":scope > .form-status") || $(".form-status", form);
      var attempted = false;
      var fields = function () { return $$("input, select, textarea", form).filter(function (el) { return el.id && el.type !== "submit"; }); };

      fields().forEach(function (el) {
        var evt = el.type === "checkbox" || el.tagName === "SELECT" ? "change" : "input";
        el.addEventListener(evt, function () { if (attempted) showError(el, validateField(el)); });
        el.addEventListener("blur", function () { if (attempted) showError(el, validateField(el)); });
      });

      form.addEventListener("submit", function (ev) {
        ev.preventDefault();
        attempted = true;
        var errors = [];
        fields().forEach(function (el) {
          var msg = validateField(el);
          showError(el, msg);
          if (msg) errors.push({ el: el, msg: msg });
        });
        if (status) { status.textContent = ""; status.classList.remove("is-error"); }

        if (errors.length) {
          if (summary) {
            var ul = $("ul", summary);
            ul.innerHTML = "";
            errors.forEach(function (er) {
              var li = document.createElement("li");
              var a = document.createElement("a");
              a.href = "#" + er.el.id;
              a.textContent = er.msg;
              a.addEventListener("click", function (e) { e.preventDefault(); er.el.focus(); });
              li.appendChild(a);
              ul.appendChild(li);
            });
            summary.hidden = false;
            summary.focus();
          } else {
            errors[0].el.focus();
          }
          return;
        }
        if (summary) summary.hidden = true;

        var submitBtn = $('[type="submit"]', form);
        if (submitBtn) submitBtn.disabled = true;
        submitForm(form).then(function (mode) {
          var msg = mode === "mailto"
            ? "Your email app should now open with your message ready to send. If nothing happens, email us at " + (CONFIG.contactEmail || "") + "."
            : null;
          if (success) {
            if (msg) {
              var p = $("[data-success-text]", success);
              if (p) p.textContent = (kind === "register" ? "Your registration details are ready. " : "") + msg;
            }
            success.hidden = false;
            form.reset();
            attempted = false;
            if (kind === "register") form.hidden = true;
            success.focus();
          } else if (status) {
            status.textContent = mode === "mailto"
              ? "Thank you! Your email app should open so you can confirm your subscription."
              : "Thank you for subscribing! Please check your inbox to confirm.";
            form.reset();
          }
        }).catch(function () {
          if (status) {
            status.textContent = "Sorry, something went wrong. Please try again or email us at " + (CONFIG.contactEmail || "") + ".";
            status.classList.add("is-error");
          }
        }).then(function () { if (submitBtn) submitBtn.disabled = false; });
      });
    });

    // Preselect values from the URL (?category=…, ?subject=…)
    var params = new URLSearchParams(window.location.search);
    [["category", "#team-category"], ["subject", "#contact-subject"]].forEach(function (p) {
      var val = params.get(p[0]);
      var sel = $(p[1]);
      if (val && sel && $$("option", sel).some(function (o) { return o.value === val; })) sel.value = val;
    });

    // Registration: reveal optional member rows one at a time
    var addBtn = $("[data-add-member]");
    if (addBtn) {
      var memberStatus = $("[data-member-status]");
      var update = function () { addBtn.hidden = !$("[data-optional-member][hidden]"); };
      addBtn.addEventListener("click", function () {
        var next = $("[data-optional-member][hidden]");
        if (!next) return;
        next.hidden = false;
        var input = $("input", next);
        if (input) input.focus();
        update();
        if (memberStatus) memberStatus.textContent = addBtn.hidden ? "Maximum of 5 team members reached." : "";
      });
      update();
    }
  }

  /* ------------------------------------------------------------------
     News filter
  ------------------------------------------------------------------ */
  function initNewsFilter() {
    var group = $(".filter-buttons");
    if (!group) return;
    var status = $("#news-status");
    var cards = $$(".news-card[data-tag]");
    group.addEventListener("click", function (ev) {
      var btn = ev.target.closest("button[data-filter]");
      if (!btn) return;
      var tag = btn.getAttribute("data-filter");
      $$("button", group).forEach(function (b) { b.setAttribute("aria-pressed", b === btn ? "true" : "false"); });
      var shown = 0;
      cards.forEach(function (c) {
        var show = !tag || c.getAttribute("data-tag") === tag;
        c.hidden = !show;
        if (show) shown++;
      });
      if (status) status.textContent = "Showing " + shown + " " + (shown === 1 ? "article" : "articles") + (tag ? " tagged " + tag : "") + ".";
    });
  }

  /* Copy link / native share on news articles */
  function initShare() {
    $$(".copy-link").forEach(function (b) {
      if (!navigator.clipboard) return;
      b.hidden = false;
      b.addEventListener("click", function () {
        navigator.clipboard.writeText(b.getAttribute("data-copy")).then(function () { announce("Link copied to clipboard"); });
      });
    });
  }

  /* ------------------------------------------------------------------
     Gallery lightbox (native <dialog>: focus trap + Escape built in)
  ------------------------------------------------------------------ */
  function initLightbox() {
    var dialog = $("dialog.lightbox");
    var links = $$("[data-lightbox]");
    if (!dialog || !links.length || typeof dialog.showModal !== "function") return;
    var img = $("img", dialog), cap = $(".lightbox-caption", dialog), count = $(".lightbox-count", dialog);
    var current = 0, opener = null;

    function show(i) {
      current = (i + links.length) % links.length;
      var link = links[current], thumb = $("img", link);
      img.src = link.getAttribute("href");
      img.alt = thumb.alt;
      cap.textContent = link.getAttribute("data-caption");
      count.textContent = "Image " + (current + 1) + " of " + links.length;
    }
    links.forEach(function (link, i) {
      link.addEventListener("click", function (ev) {
        ev.preventDefault();
        opener = link;
        show(i);
        dialog.showModal();
        $('[data-lb="close"]', dialog).focus();
      });
    });
    dialog.addEventListener("click", function (ev) {
      var b = ev.target.closest("[data-lb]");
      if (ev.target === dialog) { dialog.close(); return; }
      if (!b) return;
      var a = b.getAttribute("data-lb");
      if (a === "close") dialog.close();
      if (a === "next") show(current + 1);
      if (a === "prev") show(current - 1);
    });
    dialog.addEventListener("keydown", function (ev) {
      if (ev.key === "ArrowRight") { show(current + 1); ev.preventDefault(); }
      if (ev.key === "ArrowLeft") { show(current - 1); ev.preventDefault(); }
    });
    dialog.addEventListener("close", function () { if (opener) links[current].focus(); });
  }

  /* ------------------------------------------------------------------
     FAQ filter + expand all
  ------------------------------------------------------------------ */
  function initFaq() {
    var input = $("[data-faq-filter]");
    var expand = $("[data-faq-expand]");
    var items = $$(".faq-item");
    if (!items.length) return;
    var status = $("#faq-status");
    if (input) {
      input.addEventListener("input", function () {
        var q = input.value.trim().toLowerCase();
        var shown = 0;
        items.forEach(function (d) {
          var match = !q || d.textContent.toLowerCase().indexOf(q) !== -1;
          d.hidden = !match;
          if (match) shown++;
          if (q && match) d.open = true;
        });
        $$(".faq-group").forEach(function (g) { g.hidden = !$$(".faq-item:not([hidden])", g).length; });
        if (status) status.textContent = q ? (shown ? shown + " matching " + (shown === 1 ? "question" : "questions") + "." : "No questions match. Try another word or contact us.") : "";
      });
    }
    if (expand) {
      expand.hidden = false;
      expand.addEventListener("click", function () {
        var open = expand.textContent.indexOf("Expand") === 0;
        items.forEach(function (d) { d.open = open; });
        expand.textContent = open ? "Collapse all answers" : "Expand all answers";
      });
    }
  }

  /* ------------------------------------------------------------------
     Past-paper practice: check answers, score Part A, toggle solutions
  ------------------------------------------------------------------ */
  function initQuiz() {
    var quiz = $("[data-quiz]");
    var toggle = $("[data-toggle-solutions]");
    if (toggle) {
      toggle.hidden = false;
      toggle.addEventListener("click", function () {
        var open = toggle.textContent.indexOf("Show") === 0;
        $$("details.solution").forEach(function (d) { d.open = open; });
        toggle.textContent = open ? "Hide all worked solutions" : "Show all worked solutions";
      });
    }
    if (!quiz) return;
    var questions = $$("[data-answer]", quiz);

    function clear(q) {
      q.classList.remove("is-correct", "is-wrong");
      $$(".opt-badge", q).forEach(function (b) { b.remove(); });
      $$(".option", q).forEach(function (o) { o.classList.remove("is-answer", "is-chosen-wrong"); });
      $(".q-feedback", q).textContent = "";
    }
    function badge(option, text) {
      var b = document.createElement("span");
      b.className = "opt-badge";
      b.textContent = text;
      $("label", option).appendChild(b);
    }
    // Returns "correct", "wrong" or "blank"
    function check(q, quiet) {
      clear(q);
      var answer = q.getAttribute("data-answer");
      var chosen = $("input:checked", q);
      var fb = $(".q-feedback", q);
      if (!chosen) {
        if (!quiet) fb.textContent = "Choose an answer first.";
        return "blank";
      }
      var right = $('input[value="' + answer + '"]', q).closest(".option");
      right.classList.add("is-answer");
      badge(right, "Correct answer");
      if (chosen.value === answer) {
        q.classList.add("is-correct");
        fb.textContent = "Correct! The answer is " + answer + ".";
        return "correct";
      }
      var mine = chosen.closest(".option");
      mine.classList.add("is-chosen-wrong");
      badge(mine, "Your answer");
      q.classList.add("is-wrong");
      fb.textContent = "Not quite. You chose " + chosen.value + "; the correct answer is " + answer + ". Open the worked solution to see why.";
      return "wrong";
    }

    questions.forEach(function (q) {
      $(".q-actions", q).hidden = false;
      $("[data-check]", q).addEventListener("click", function () { check(q); });
      // Changing the selection clears old feedback
      $$("input", q).forEach(function (r) {
        r.addEventListener("change", function () { if (q.classList.contains("is-correct") || q.classList.contains("is-wrong")) clear(q); });
      });
    });

    var scoreBox = $(".quiz-score", quiz);
    if (!scoreBox) return;
    scoreBox.hidden = false;
    var result = $(".quiz-result", scoreBox);
    $("[data-check-all]", scoreBox).addEventListener("click", function () {
      var counts = { correct: 0, wrong: 0, blank: 0 };
      questions.forEach(function (q) { counts[check(q, true)]++; });
      result.textContent = "You scored " + counts.correct * 2 + " out of " + questions.length * 2 + " marks: " +
        counts.correct + " correct, " + counts.wrong + " incorrect" +
        (counts.blank ? ", " + counts.blank + " not answered" : "") + ".";
    });
    $("[data-reset]", scoreBox).addEventListener("click", function () {
      questions.forEach(function (q) { clear(q); $$("input", q).forEach(function (r) { r.checked = false; }); });
      $$("details.solution", quiz).forEach(function (d) { d.open = false; });
      result.textContent = "Answers cleared.";
      var first = $("input", questions[0]);
      if (first) first.focus();
    });
  }

  /* Prefill the header search box on the search page */
  function initSearchBox() {
    var q = new URLSearchParams(window.location.search).get("q");
    var box = $("#site-search-q");
    if (q && box && document.body.getAttribute("data-page") === "search") box.value = q;
  }

  window.SO = { announce: announce, $: $, $$: $$ };

  var booted = false;
  function boot() {
    if (booted) return;
    booted = true;
    initA11yPanel();
    initNav();
    initAnchors();
    initCountdowns();
    initTimeline();
    initForms();
    initNewsFilter();
    initShare();
    initLightbox();
    initFaq();
    initSearchBox();
    initQuiz();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
