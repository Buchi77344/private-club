const hamburger = document.querySelector(".hamburger")
const mobileNav = document.querySelector(".mobile-nav");
const overlay = document.querySelector("header .overlay");
const closeNavBtn = document.querySelector(".close-nav-btn")


hamburger.addEventListener("click", () => {
    overlay.style.display= "block"
    setTimeout(() => {
        overlay.classList.add("reveal")
        mobileNav.classList.add("slideIn");
    }, 100)
})

closeNavBtn.addEventListener("click", () => {
    overlay.classList.remove("reveal");
    mobileNav.classList.remove("slideIn");
    setTimeout(() => {
        overlay.style.display = "none";
	}, 500);
});