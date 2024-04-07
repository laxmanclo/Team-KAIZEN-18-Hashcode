const loginForm = document.querySelector('.login-form');

loginForm.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent default form submission

  // Here, you'd handle form data (email/password) and send it to your backend for authentication
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  // Simulate sending data to backend (replace with actual logic)
  fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password })
  })
  .then(response => {
    if (response.ok) {
      // Login successful, redirect or display success message
      console.log('Login successful!');
    } else {
      // Login failed, display error message
      console.error('Login failed!');
    }
  });
});
