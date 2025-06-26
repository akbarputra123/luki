document.addEventListener('DOMContentLoaded', function() {
    // Toggle password visibility
    const togglePassword = document.querySelector('#togglePassword');
    const password = document.querySelector('#password');
    
    if (togglePassword && password) {
        togglePassword.addEventListener('click', function() {
            // Toggle the type attribute
            const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
            password.setAttribute('type', type);
            
            // Toggle the eye icon
            this.classList.toggle('fa-eye');
            this.classList.toggle('fa-eye-slash');
        });
    }
    
    // Form submission handling
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // You can add form validation here if needed
            // e.preventDefault(); // Uncomment to prevent default submission for AJAX
            
            // Add loading state
            const submitButton = this.querySelector('button[type="submit"]');
            if (submitButton) {
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                submitButton.disabled = true;
            }
            
            // If not using AJAX, the form will submit normally
            // For AJAX submission, you would handle the response here
        });
    }
    
    // Add animation to input fields when focused
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.querySelector('i').style.color = '#4a90e2';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.querySelector('i').style.color = '#777';
        });
    });
});