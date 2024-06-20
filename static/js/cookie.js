// Function to show the cookie consent banner
function showCookieBanner() {
  var banner = document.getElementById('cookie-consent-banner');
  banner.style.display = 'block';
}

// Function to hide the cookie consent banner
function hideCookieBanner() {
  var banner = document.getElementById('cookie-consent-banner');
  banner.style.display = 'none';
}

// Check if user has already made a choice (cookie exists)
function checkCookieConsent() {
  var cookieConsent = getCookie('cookieConsent');
  if (cookieConsent === 'accepted' || cookieConsent === 'denied') {
      // If user has already made a choice, hide the banner
      hideCookieBanner();
  } else {
      // If no cookie exists, show the banner
      showCookieBanner();
  }
}

// Event listener for accepting cookies
document.getElementById('accept-cookies').addEventListener('click', function() {
  // Set a cookie to remember the user's choice
  setCookie('cookieConsent', 'accepted', 365);
  // Hide the cookie consent banner
  hideCookieBanner();
});

// Event listener for denying cookies
document.getElementById('deny-cookies').addEventListener('click', function() {
  // Set a cookie to remember the user's choice
  setCookie('cookieConsent', 'denied', 365);
  // Hide the cookie consent banner
  hideCookieBanner();
});

// Function to set a cookie
function setCookie(name, value, days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

// Function to get a cookie
function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0) == ' ') {
          c = c.substring(1, c.length);
      }
      if (c.indexOf(nameEQ) == 0) {
          return c.substring(nameEQ.length, c.length);
      }
  }
  return null;
}

// When the page loads, check if the user has already made a choice
window.onload = function() {
  checkCookieConsent();
};