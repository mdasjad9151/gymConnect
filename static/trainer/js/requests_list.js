function showGymUsers(gymId) {
  fetch(`/gym-trainer/gym/${gymId}/`)
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("gym-user-list");
      container.innerHTML = "";

      if (data.gyms.length === 0) {
        container.innerHTML =
          "<p class='text-gray-700'>No gyms found for this gym owner.</p>";
      } else {
        data.gyms.forEach((gym) => {
          const div = document.createElement("div");
          div.classList = "border-b border-gray-300 py-2 px-2";
          div.innerHTML = `
              <div class="font-semibold text-red-700">${gym.name}</div>
              <div class="text-sm text-gray-700">
                ${gym.address}, ${gym.city}, ${gym.state} - ${gym.pincode}
              </div>
              <div class="text-sm text-gray-600 mt-1">
                Rating: ${gym.average_rating} (${gym.rating_count} reviews)<br>
                Price per day: ₹${gym.price_per_day}
              </div>
            `;
          container.appendChild(div);
        });
      }

      document.getElementById("gym-details-popup").style.display = "flex";
    })
    .catch((error) => {
      console.error("Error fetching gym data:", error);
      alert("Failed to fetch gym details.");
    });
}

function closePopup() {
  document.getElementById("gym-details-popup").style.display = "none";
}
