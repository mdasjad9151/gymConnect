// Function to show the success message
function showSuccessMessage(message) {
  const messageElement = document.getElementById("success-message");
  const successText = document.getElementById("success-text");

  successText.textContent = message;

  // Show the message and fade it in
  messageElement.style.display = "block";
  setTimeout(() => {
    messageElement.style.opacity = 1;
  }, 10); // Delay to allow the transition to work

  // Hide the message after 5 seconds
  setTimeout(() => {
    setTimeout(() => {
      messageElement.style.display = "none";
    }, 500); // Wait for the fade-out transition to complete
  }, 5000); // Wait for 5 seconds before hiding
}
// Function to open the popup with trainer details
function openTrainerPopup(trainerId) {
  console.log(`/gym-owner/get-trainer-details/${trainerId}/`);
  fetch(`/gym-owner/get-trainer-details/${trainerId}/`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("trainer-name").textContent = data.name;
      document.getElementById("trainer-address").textContent = data.address;
      document.getElementById("trainer-contact").textContent = data.contact_no;
      document.getElementById("trainer-gym").textContent = data.gym_name;
      document.getElementById("trainer-gym-address").textContent =
        data.gym_address;
      document.getElementById("trainer-certificate").href =
        data.certificate_link;

      if (data.image_url) {
        document.getElementById("trainer-image").src = data.image_url;
        document.getElementById("trainer-image").style.display = "block";
      } else {
        document.getElementById("trainer-image").style.display = "none";
      }

      // Set the trainer ID in the hidden input
      document.getElementById("trainer-id").value = trainerId;

      // Show the popup and overlay
      document.getElementById("popup").style.display = "block";
      document.getElementById("overlay").style.display = "block";
    })
    .catch((error) => console.error("Error:", error));
}

// Function to close the popup
function closePopup() {
  document.getElementById("popup").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

// Function to send a connection request from the trainer list
function sendConnectionRequest(trainerId) {
  const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  console.log(csrftoken);
  // Check if the csrftoken is properly fetched
  if (!csrftoken) {
    console.error("CSRF token not found!");
    return;
  }

  const trainerItem = document.querySelector(
    `[data-trainer-id="${trainerId}"]`
  );

  if (!trainerItem) {
    console.error("Trainer item not found!");
    return;
  }

  const connectButton = trainerItem.querySelector("button"); // Get the "Connect" button
  console.log(connectButton);
  fetch(`/gym-owner/create-trainer-request/`, {
    method: "POST", // Ensure POST method is used
    headers: {
      "Content-Type": "application/json", // Send as JSON
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ trainer_id: trainerId }), // Send trainer_id as JSON
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.message) {
        // Remove the trainer item from the list
        trainerItem.remove(); // Removes the trainer's entry from the DOM

        // Optionally, you can display a message or alert the user about the successful request
        // Display the success message
        showSuccessMessage("Request Sent Successfully!");
      } else {
        alert(data.error);
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Function to send a connection request from the popup
function sendConnectionRequestPopup() {
  const trainerId = document.getElementById("trainer-id").value; // Get trainer ID from the hidden input
  sendConnectionRequest(trainerId);
  closePopup();
}

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
