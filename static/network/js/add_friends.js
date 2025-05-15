
function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}
document.querySelectorAll(".add-friend-btn").forEach((button) => {
  button.addEventListener("click", function () {
    const userId = this.getAttribute("data-id");

    fetch(`/network/add_friend/${userId}/`, {
      method: "POST",
      headers: { "X-CSRFToken": getCsrfToken() },
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          this.innerText = "Requested";
          this.classList.replace("bg-[#9e3532]", "bg-gray-500");
          this.classList.replace("hover:bg-[#71211C]", "hover:bg-gray-600");
          this.disabled = true;
        }
      });
  });
});


// Search function to filter trainers
function searchTrainers() {
  const input = document.getElementById("search-input").value.toLowerCase();
  const trainerItems = document.querySelectorAll(".trainer-item");

  trainerItems.forEach((item) => {
    const trainerName = item.querySelector("h2").textContent.toLowerCase();

    // If the trainer name includes the search input, show the item, otherwise hide it
    if (trainerName.includes(input)) {
      item.classList.remove("hidden"); // Show by removing hidden class
    } else {
      item.classList.add("hidden"); // Hide by adding hidden class
    }
  });
}