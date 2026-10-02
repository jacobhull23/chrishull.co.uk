// Shared by every page.
(function () {
  // Keep the footer copyright year current without editing HTML.
  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();

  // Light protection for the paintings: no right-click "Save image" and no dragging them
  // off the page. It only deters casual copying (and is easy to bypass), so instead of a
  // blunt block it shows a friendly note pointing people to the contact page.
  var PROTECTED = '.frame, .lb-stage';
  var note = null, timer = null;

  function showNote() {
    if (!note) {
      note = document.createElement('div');
      note.className = 'copy-note';
      note.setAttribute('role', 'status');
      note.innerHTML = 'These paintings are my own work and protected by copyright. ' +
        'If you’d like to use one, please <a href="contact.html">get in touch</a>.';
      // The lightbox is a modal <dialog>; put the note inside it when it's open so it shows on top.
      document.body.appendChild(note);
    }
    var lb = document.getElementById('lightbox');
    (lb && lb.open ? lb : document.body).appendChild(note);
    note.classList.add('show');
    clearTimeout(timer);
    timer = setTimeout(function () { note.classList.remove('show'); }, 4000);
  }

  document.addEventListener('contextmenu', function (e) {
    if (e.target.closest && e.target.closest(PROTECTED)) {
      e.preventDefault();
      showNote();
    }
  });
  document.addEventListener('dragstart', function (e) {
    if (e.target.closest && e.target.closest(PROTECTED)) e.preventDefault();
  });
})();
