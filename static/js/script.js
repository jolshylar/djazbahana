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
if (conversationThread)
  conversationThread.scrollTop = conversationThread.scrollHeight;

// Toggle light theme
const themeSwitcher = document.getElementById("theme-switch");

let logo = document.getElementById("logo");
themeSwitcher.checked = true;

function toggleTheme() {
  let curTheme = (this.checked) ? "light" : "dark";
  let oldTheme = (this.checked) ? "dark" : "light";

  document.body.classList.replace(oldTheme, curTheme);
  localStorage.setItem("theme", curTheme);
  logo.src = `../images/logo_${curTheme}.png`;
}

themeSwitcher.addEventListener("click", toggleTheme);

window.onload = checkTheme();

function checkTheme() {
  const localStorageTheme = localStorage.getItem("theme");

  if (localStorageTheme !== null) {
    document.body.className = localStorageTheme;
    const themeSwitch = document.getElementById("theme-switch");
    checked = (localStorageTheme === "light") ? true : false;
    themeSwitch.checked = checked;
    logo.src = `../images/logo_${localStorageTheme}.png`
  }
}

// Hamburger-menu script
let menu = document.getElementById("menu");
let navi = document.getElementById("bar");
let wrapper = document.getElementById("list-wrapper");
let counter = 3;

function hamburgerMenu() {
  if (counter % 2 == 1) {
    counter++;
    navi.classList.add("change");
    wrapper.classList.remove("list-wrapper");
  } else {
    counter++;
    navi.classList.remove("change");
    wrapper.classList.add("list-wrapper");
  }
}
