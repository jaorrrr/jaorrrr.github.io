/* Participating schools: text/country filter and an optional map.
   The map (Leaflet + OpenStreetMap) is only downloaded when the visitor asks for it. */
(function () {
  "use strict";
  var form = document.querySelector("[data-school-filter]");
  var list = document.getElementById("school-list");
  if (!form || !list) return;
  var q = document.getElementById("school-q");
  var country = document.getElementById("school-country");
  var status = document.getElementById("school-status");
  var items = Array.prototype.slice.call(list.children);
  var data = JSON.parse(document.getElementById("school-data").textContent);
  var map = null, markers = [];

  form.addEventListener("submit", function (ev) { ev.preventDefault(); });

  function apply() {
    var text = q.value.trim().toLowerCase();
    var c = country.value;
    var shown = 0;
    items.forEach(function (li) {
      var ok = (!c || li.getAttribute("data-country") === c) &&
               (!text || li.getAttribute("data-name").indexOf(text) !== -1);
      li.hidden = !ok;
      if (ok) shown++;
    });
    status.textContent = shown === items.length
      ? "Showing all " + shown + " institutions."
      : shown === 0 ? "No institutions match your filters."
      : "Showing " + shown + " of " + items.length + " institutions.";
    if (map) updateMarkers();
  }
  var t;
  q.addEventListener("input", function () { clearTimeout(t); t = setTimeout(apply, 250); });
  country.addEventListener("change", apply);

  /* ---- Map ---- */
  var btn = document.querySelector("[data-map-toggle]");
  var wrap = document.getElementById("school-map-wrap");
  if (!btn || !wrap) return;
  btn.hidden = false;
  var label = btn.querySelector("span");

  function loadLeaflet() {
    return new Promise(function (resolve, reject) {
      if (window.L) return resolve();
      var css = document.createElement("link");
      css.rel = "stylesheet";
      css.href = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css";
      document.head.appendChild(css);
      var s = document.createElement("script");
      s.src = "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js";
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  function esc(s) { var d = document.createElement("div"); d.textContent = s; return d.innerHTML; }

  function updateMarkers() {
    var text = q.value.trim().toLowerCase(), c = country.value, bounds = [];
    markers.forEach(function (m) {
      var d = m.school;
      var ok = (!c || d.country === c) && (!text || (d.name + " " + d.city).toLowerCase().indexOf(text) !== -1);
      if (ok) { m.addTo(map); bounds.push([d.lat, d.lng]); } else m.remove();
    });
    if (bounds.length) map.fitBounds(bounds, { padding: [30, 30], maxZoom: 6 });
  }

  function initMap() {
    map = L.map("school-map", { scrollWheelZoom: false, worldCopyJump: true });
    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    markers = data.map(function (d) {
      var m = L.marker([d.lat, d.lng], { title: d.name + ", " + d.city + ", " + d.country, alt: d.name, keyboard: true });
      m.bindPopup("<strong>" + esc(d.name) + "</strong><br>" + esc(d.city) + ", " + esc(d.country) + "<br>" + esc(d.type));
      m.school = d;
      return m;
    });
    updateMarkers();
  }

  btn.addEventListener("click", function () {
    var open = btn.getAttribute("aria-expanded") !== "true";
    btn.setAttribute("aria-expanded", open ? "true" : "false");
    label.textContent = open ? "Hide map" : "Show map";
    wrap.hidden = !open;
    if (open && !map) {
      label.textContent = "Loading map…";
      loadLeaflet().then(function () {
        label.textContent = "Hide map";
        initMap();
      }).catch(function () {
        label.textContent = "Show map";
        btn.setAttribute("aria-expanded", "false");
        wrap.hidden = true;
        status.textContent = "The map could not be loaded. All institutions are listed below.";
      });
    } else if (open && map) {
      map.invalidateSize();
    }
  });
})();
