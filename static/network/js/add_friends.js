
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