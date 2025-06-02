let gymUserId;


function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

function openPlanPopup(userId) {
  gymUserId = userId;
  fetch(`/gym-trainer/get-user-plan/${userId}`)
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("update-date").innerText =
        data.update_date || "NA";
      loadPreviousItems("monday", data.monday_workout);
      loadPreviousItems("tuesday", data.tuesday_workout);
      loadPreviousItems("wednesday", data.wednesday_workout);
      loadPreviousItems("thursday", data.thursday_workout);
      loadPreviousItems("friday", data.friday_workout);
      loadPreviousItems("saturday", data.saturday_workout);
      loadPreviousItems("breakfast", data.breakfast);
      loadPreviousItems("lunch", data.lunch);
      loadPreviousItems("dinner", data.dinner);
      loadPreviousItems("preworkout_diet", data.preworkout_diet);

      document.getElementById("plan-popup").style.display = "block";
      document.getElementById("plan-popup").style.display = "mt-[7rem]";
    });
}

function loadPreviousItems(field, items) {
  const container = document.getElementById(`${field}_div`);

  if (items === "") {
    console.log("shjhujanfe");
  } else {
    items.split(",").forEach((item) => addItemToContainer(field, item));
  }
}

function addItem(field) {
  const input = document.getElementById(`${field}`);
  console.log(input);
  const item = input.value;
  console.log(item);
  if (item) {
    addItemToContainer(field, item);
    input.value = ""; // Clear input field
  }
}

function addItemToContainer(field, item) {
  const container = document.getElementById(`${field}_div`);
  const itemDiv = document.createElement("div");
  itemDiv.classList.add("item"); // Optional: Add a class for styling

  // Add the item text
  const itemText = document.createElement("span");
  itemText.innerText = item;
  itemDiv.appendChild(itemText);

  // Create the remove button with an image (cross.png)
  const removeBtn = document.createElement("button");
  removeBtn.classList.add("remove-btn"); // Optional: Add a class for styling

  const removeImg = document.createElement("img");
  removeImg.src = crossImgUrl; // Replace with actual path
  removeImg.alt = "Remove"; // Alt text for accessibility
  removeImg.classList.add("remove-img"); // Add a class for styling the image size

  // Style the image to match the font size
  removeImg.style.width = "1em"; // Set width to font-size
  removeImg.style.height = "1em"; // Set height to font-size

  // Append the image to the button
  removeBtn.appendChild(removeImg);

  // Set up the remove button functionality
  removeBtn.onclick = () => itemDiv.remove();

  // Append the remove button to the item div
  itemDiv.appendChild(removeBtn);

  // Append the item div to the container
  container.appendChild(itemDiv);
}

function submitPlan() {
  const fields = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "breakfast",
    "lunch",
    "dinner",
    "preworkout_diet",
  ];
  const formData = new FormData();

  fields.forEach((field) => {
    const items = Array.from(document.getElementById(`${field}_div`).children)
      .map((div) => div.firstChild.textContent)
      .join(",");
    formData.append(`${field}_div`, items);
  });

  formData.append("gym_user_id", gymUserId);

  fetch("/gym-trainer/update-plan/", {
    method: "POST",
    body: formData,
    headers: { "X-CSRFToken": getCsrfToken() },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) closePopup();
    });
}

function closePopup() {
  document.getElementById("plan-popup").style.display = "none";
}
