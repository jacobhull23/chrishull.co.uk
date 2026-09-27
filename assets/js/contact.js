// Contact form: prefills the painting from ?painting=, submits via FormSubmit's
// AJAX endpoint so the visitor stays on the page. Without JavaScript the form
// posts normally and FormSubmit redirects back with ?sent=1.
(function () {
  'use strict';

  var form = document.getElementById('enquiry');
  var success = document.getElementById('form-success');
  var errorBox = document.getElementById('form-error');
  var submit = form.querySelector('button[type="submit"]');
  var params = new URLSearchParams(location.search);

  var painting = params.get('painting');
  if (painting) {
    document.getElementById('painting').value = painting.slice(0, 200);
    form.querySelector('[name="_subject"]').value = 'Painting enquiry: ' + painting.slice(0, 120);
  }

  function showSuccess() {
    form.hidden = true;
    success.hidden = false;
    success.querySelector('h2').focus();
  }

  if (params.get('sent') === '1') {
    showSuccess();
    params.delete('sent');
    var qs = params.toString();
    history.replaceState(null, '', location.pathname + (qs ? '?' + qs : ''));
  }

  function showError(msg) {
    errorBox.textContent = msg;
    errorBox.hidden = false;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    errorBox.hidden = true;
    var formId = form.dataset.formId;

    if (!formId || formId === 'FORMSUBMIT_ID') {
      showError('Sorry, the enquiry form isn’t connected yet. Please try again soon.');
      return;
    }

    submit.disabled = true;
    submit.textContent = 'Sending…';
    fetch('https://formsubmit.co/ajax/' + encodeURIComponent(formId), {
      method: 'POST',
      headers: { Accept: 'application/json' },
      body: new FormData(form)
    })
      .then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (data) {
          if (!res.ok || String(data.success) !== 'true') throw new Error(data.message || res.status);
        });
      })
      .then(function () {
        form.reset();
        showSuccess();
      })
      .catch(function () {
        showError('Sorry, your message couldn’t be sent. Please check your connection and try again.');
      })
      .then(function () {
        submit.disabled = false;
        submit.textContent = 'Send enquiry';
      });
  });

  document.getElementById('send-another').addEventListener('click', function () {
    success.hidden = true;
    form.hidden = false;
    document.getElementById('name').focus();
  });
})();
