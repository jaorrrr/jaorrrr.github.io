/* Client-side site search over assets/data/search-index.json */
(function () {
  "use strict";
  var form = document.querySelector("[data-search-form]");
  var input = document.getElementById("search-page-q");
  var status = document.getElementById("search-status");
  var list = document.getElementById("search-results");
  if (!form || !input || !list) return;

  var index = null;

  function esc(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function terms(q) {
    return q.toLowerCase().split(/\s+/).filter(function (t) { return t.length > 1; });
  }
  function highlight(text, ts) {
    var out = esc(text);
    ts.forEach(function (t) {
      var re = new RegExp("(" + esc(t).replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "gi");
      out = out.replace(re, "<mark>$1</mark>");
    });
    return out;
  }
  function snippet(text, ts) {
    var lower = text.toLowerCase();
    var pos = -1;
    ts.some(function (t) { pos = lower.indexOf(t); return pos !== -1; });
    var start = Math.max(0, pos - 60);
    var s = text.slice(start, start + 200);
    return (start > 0 ? "…" : "") + s + (start + 200 < text.length ? "…" : "");
  }

  function run(q) {
    var ts = terms(q);
    list.innerHTML = "";
    if (!ts.length) { status.textContent = "Enter a word or phrase to search."; return; }
    var results = index.map(function (e) {
      var title = e.title.toLowerCase(), text = e.text.toLowerCase(), score = 0;
      var all = ts.every(function (t) {
        var hit = false;
        if (title.indexOf(t) !== -1) { score += 5; hit = true; }
        var count = text.split(t).length - 1;
        if (count) { score += Math.min(count, 5); hit = true; }
        return hit;
      });
      return all ? { e: e, score: score } : null;
    }).filter(Boolean).sort(function (a, b) { return b.score - a.score; }).slice(0, 25);

    status.textContent = results.length
      ? results.length + (results.length === 1 ? " result" : " results") + " for “" + q + "”."
      : "No results for “" + q + "”. Try a different word, or browse the FAQ.";
    results.forEach(function (r) {
      var li = document.createElement("li");
      var heading = r.e.title === r.e.page ? r.e.title : r.e.title;
      li.innerHTML = '<h3><a href="' + esc(r.e.url) + '">' + highlight(heading, ts) + "</a></h3>" +
        '<p class="result-page">' + esc(r.e.page) + "</p>" +
        "<p>" + highlight(snippet(r.e.text, ts), ts) + "</p>";
      list.appendChild(li);
    });
    document.title = "Search results for “" + q + "” | Sustainable Olympiad";
  }

  var initial = new URLSearchParams(window.location.search).get("q") || "";
  input.value = initial;
  status.textContent = initial ? "Searching…" : "Enter a word or phrase to search.";

  fetch("assets/data/search-index.json")
    .then(function (r) { return r.json(); })
    .then(function (data) { index = data; if (initial) run(initial); })
    .catch(function () { status.textContent = "Search is unavailable right now. Please browse using the main menu."; });

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var q = input.value.trim();
    if (!index) return;
    history.replaceState(null, "", "search.html" + (q ? "?q=" + encodeURIComponent(q) : ""));
    run(q);
  });
})();
