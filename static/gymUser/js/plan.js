function toggleSection(sectionId) {
  const section = document.getElementById(sectionId);
  const maxHeight = section.style.maxHeight;
  section.style.maxHeight = maxHeight ? null : section.scrollHeight + "px";
}

// Function to show loading overlay
function showLoading() {
  document.getElementById("loading-overlay").classList.remove("hidden");
  setTimeout(
    () => document.getElementById("loading-overlay").classList.add("hidden"),
    1000
  ); // Simulating load time
}

// Show loading when the page is loaded
window.onload = showLoading;
