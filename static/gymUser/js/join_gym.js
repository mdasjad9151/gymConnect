    function joinGym(gymId) {
      const joinButton = document.getElementById(`join-btn-${gymId}`);
      joinButton.disabled = true;
      joinButton.innerHTML = `<svg class="animate-spin h-5 w-5 mr-2 text-white inline" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v3.5a4.5 4.5 0 100 9V20a8 8 0 01-8-8z"></path>
    </svg> Joining...`;

      fetch(`/gym-user/join-gym/${gymId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfId,
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            document
              .getElementById("success-message")
              .classList.remove("hidden");
            joinButton.innerHTML = "Joined";
            joinButton.classList.add("bg-green-500");
            joinButton.classList.remove(
              "bg-[#4399c5]",
              "hover:bg-[#cbccc6]/10",
              "hover:text-black"
            );
          }
        })
        .catch((error) => console.error("Error:", error));
    }

    function closeMessage() {
      document.getElementById("success-message").classList.add("hidden");
    }
