// Shared by every page: keep the footer copyright year current without editing HTML.
(function () {
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
