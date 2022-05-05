const dropdownMenu = document.querySelector(".dropdown-menu");
const dropdownButton = document.querySelector(".dropdown-button");

if (dropdownButton) {
  dropdownButton.addEventListener("click", () => {
    dropdownMenu.classList.toggle("show");
  });
}

// Upload Image
const photoInput = document.querySelector("#avatar");
const photoPreview = document.querySelector("#preview-avatar");
if (photoInput)
  photoInput.onchange = () => {
    const [file] = photoInput.files;
    if (file) {
      photoPreview.src = URL.createObjectURL(file);
    }
  };

// Scroll to Bottom
const conversationThread = document.querySelector(".classroom__box");
if (conversationThread) conversationThread.scrollTop = conversationThread.scrollHeight;

// Toggle light theme
const themeSwitcher = document.getElementById("theme-switch");

let logo = document.getElementById("logo")
themeSwitcher.checked = false;

function toggleTheme() {
  if (this.checked) {
    // document.body.setAttribute('theme', 'dark');
    document.body.classList.remove("light");
    document.body.classList.add("dark");
    localStorage.setItem("theme", "dark");
    logo.src = "../images/logo_dark.png";
  } else {
    // document.body.setAttribute('theme', 'light');
    document.body.classList.add("light");
    document.body.classList.remove("dark");
    localStorage.setItem("theme", "light");
    logo.src = "../images/logo_light.png";
  }
}
themeSwitcher.addEventListener("click", toggleTheme);

window.onload = checkTheme();

function checkTheme() {
  const localStorageTheme = localStorage.getItem("theme")

  if (localStorageTheme !== null && localStorageTheme === "dark") {
    document.body.className = localStorageTheme;

    const themeSwitch = document.getElementById("theme-switch");
    themeSwitch.checked = true;
  }
}

// // Hamburger-menu script
// let menu = document.querySelector(".menu");
// let navi = document.querySelector(".bar");

// function hamburgerMenu () {
//   navi.toggleClass("change");
// };