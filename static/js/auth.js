// EASY attr Params. to use
// class: input-wrapper --> For password hide & show toggles (gogle specific)
// id: typing-text --> For animated JS typing; required you placed the 'value' in a hidden input with id 'typed-text'

function enablePasswordToggle(wrapperClass) {
    // Find all wrappers with the given class
    const wrappers = document.querySelectorAll(`.${wrapperClass}`);

    wrappers.forEach(wrapper => {
        const input = wrapper.querySelector('input[type="password"], input[type="text"]');
        const toggleIcon = wrapper.querySelector('.toggle-password');

        if (!input || !toggleIcon) return;

        toggleIcon.addEventListener('click', () => {
            const isHidden = input.type === 'password';
            input.type = isHidden ? 'text' : 'password';

            // Swap Font Awesome icons (eye ↔ eye-slash)
            toggleIcon.classList.toggle('fa-eye');
            toggleIcon.classList.toggle('fa-eye-slash');
        });
    });
}

enablePasswordToggle('input-wrapper');

document.addEventListener("DOMContentLoaded", function() {
  const text = document.getElementById("typed-text").value;
  const el = document.getElementById("typing-text");
  let i = 0;
  let forward = true;

  function type() {
    if (forward) {
      if (i < text.length) {
        el.textContent = text.slice(0, ++i);
        setTimeout(type, 150);
      } else {
        forward = false;
        setTimeout(type, 1000);
      }
    } else {
      if (i > 0) {
        el.textContent = text.slice(0, --i);
        setTimeout(type, 100);
      } else {
        forward = true;
        setTimeout(type, 500);
      }
    }
  }

  type();

});
