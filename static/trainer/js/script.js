let gymUserId;

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
    headers: { "X-CSRFToken": "{{ csrf_token }}" },
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) closePopup();
    });
}

function closePopup() {
  document.getElementById("plan-popup").style.display = "none";
}
