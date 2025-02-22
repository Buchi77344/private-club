const hamburger = document.querySelectorAll(".hamburger")
const mobileNav = document.querySelector(".mobile-nav");
const overlay = document.querySelector(".overlay-util");
const closeNavBtn = document.querySelector(".close-nav-btn");
const accountDropdownHead = document.querySelector(".account-dropdown-head");

hamburger.forEach(ham => {
    ham.addEventListener("click", () => {
        overlay.style.display = "block";
        document.body.classList.add("no-scroll")
        setTimeout(() => {
            overlay.classList.add("reveal");
            mobileNav.classList.add("slideIn");
        }, 100);
    });
})

closeNavBtn.addEventListener("click", () => {
        document.body.classList.remove("no-scroll");
    overlay.classList.remove("reveal");
    mobileNav.classList.remove("slideIn");
    setTimeout(() => {
        overlay.style.display = "none";
	}, 500);
});

function toggleDropdown() {
    const dropdown = document.querySelector(".dropdown-util");
    // Check if dropdown is visible
    if (dropdown.style.display === "none" || dropdown.style.display === "") {
			dropdown.style.display = "block"; // Show dropdown
			const maxHeight = dropdown.scrollHeight + 10 + "px"; // Get actual height of dropdown
			dropdown.style.maxHeight = maxHeight; // Set max-height to the dropdown's height
			dropdown.style.height = maxHeight; // Set max-height to the dropdown's height
		} else {
        dropdown.style.maxHeight = "0"; // Collapse dropdown
        setTimeout(() => {
            dropdown.style.display = "none"; // Hide after transition
        }, 300); // Time matches transition duration
    }
}

		// Bind click event
		document
			.querySelector(".dropdown-toggle-util")
			.addEventListener("click", toggleDropdown);