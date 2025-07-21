document.addEventListener("DOMContentLoaded", function() {
    const passwordToggles = document.querySelectorAll('.password-toggle');
    
    passwordToggles.forEach(toggle => {
      toggle.addEventListener('click', function() {
        const input = this.closest('.password-wrapper').querySelector('input');
        const icon = this.querySelector('i');
        
        if (input.type === 'password') {
          input.type = 'text';
          icon.classList.remove('ti-eye-off');
          icon.classList.add('ti-eye');
        } else {
          input.type = 'password';
          icon.classList.remove('ti-eye');
          icon.classList.add('ti-eye-off');
        }
      });
    });
  });