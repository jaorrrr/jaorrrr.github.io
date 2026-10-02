/* Runs before first paint: applies saved accessibility preferences so the page never flashes. */
(function () {
  var root = document.documentElement;
  root.className += " js";
  var prefs = {};
  try { prefs = JSON.parse(localStorage.getItem("so-a11y") || "{}") || {}; } catch (e) { prefs = {}; }
  if (prefs.theme === "dark" || prefs.theme === "light") root.setAttribute("data-theme", prefs.theme);
  if (prefs.contrast) root.setAttribute("data-contrast", "high");
  if (prefs.spacing) root.setAttribute("data-spacing", "wide");
  if (prefs.links) root.setAttribute("data-links", "highlight");
  if (prefs.font && prefs.font !== 100) root.style.fontSize = prefs.font + "%";
  // First guess for the hamburger menu before layout (main.js then measures the real fit)
  var scale = (prefs.font || 100) / 100 * (prefs.spacing ? 1.25 : 1);
  if (window.innerWidth < 1200 * scale) root.className += " nav-compact";
})();
