// get CSRF token form the HTML meta data
function getCsrfToken() {
  return document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
}

function closeModal() {
  document.getElementById("resultModal").classList.add("hidden");
}

function showModal(data) {
  const content = `
      <p><strong>Name:</strong> ${data.name}</p>
      <p><strong>Gym:</strong> ${data.gym_name}</p>
      <p><strong>Token:</strong> ${data.token_code}</p>
      <p><strong>Paid:</strong> ${data.paid ? "Yes" : "No"}</p>
      <p><strong>Start Date:</strong> ${data.start_date}</p>
      <p><strong>Expire Date:</strong> ${data.expire_date}</p>
      <p><strong>Status:</strong> ${data.status}</p>
    `;
  document.getElementById("membershipData").innerHTML = content;
  document.getElementById("resultModal").classList.remove("hidden");
}

function startQRScanner() {
  const html5QrCode = new Html5Qrcode("reader");
  const qrCodeSuccessCallback = (decodedText, decodedResult) => {
    html5QrCode.stop();
    fetch("/membership/verify-membership-qr/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-CSRFToken": getCsrfToken(),
      },
      body: `token_code=${encodeURIComponent(decodedText)}`,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showModal(data);
        } else {
          alert(data.message);
        }
        setTimeout(
          () =>
            html5QrCode.start(
              { facingMode: "environment" },
              config,
              qrCodeSuccessCallback
            ),
          3000
        );
      })
      .catch((err) => alert("Error verifying QR"));
  };

  const config = { fps: 10, qrbox: 250 };
  html5QrCode.start(
    { facingMode: "environment" },
    config,
    qrCodeSuccessCallback
  );
}

document.addEventListener("DOMContentLoaded", startQRScanner);
