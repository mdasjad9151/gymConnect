const video = document.getElementById("video");
const playPauseBtn = document.getElementById("playPauseBtn");
const fullscreenBtn = document.getElementById("fullscreenBtn");
const muteBtn = document.getElementById("muteBtn");
const progressBar = document.getElementById("progressBar");
const durationDisplay = document.getElementById("durationDisplay");
const speedSelect = document.getElementById("speedSelect");
const qualitySelect = document.getElementById("qualitySelect");
const controlsBar = document.getElementById("controlsBar");

let mediaSource = new MediaSource();
let sourceBuffer;
let ws;
let queue = [];
let currentTime = 0;
let totalDuration = 0;

// === Format time as mm:ss ===
function formatTime(seconds) {
  const min = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const sec = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${min}:${sec}`;
}

// === Update duration & progress ===
function updateDuration() {
  const current = formatTime(video.currentTime || 0);
  const total = formatTime(totalDuration || video.duration || 0);
  durationDisplay.textContent = `${current} / ${duration}`;
  progressBar.value = (video.currentTime / (duration || 1)) * 100;
}

video.addEventListener("loadedmetadata", () => {
  totalDuration = duration;
});

video.addEventListener("timeupdate", updateDuration);

// === Stream video over WebSocket with MediaSource ===
function startStream(quality) {
  currentTime = video.currentTime;

  if (ws) ws.close();

  if (sourceBuffer && mediaSource.readyState === "open") {
    try {
      mediaSource.removeSourceBuffer(sourceBuffer);
    } catch (e) {
      console.warn("Can't remove old sourceBuffer", e);
    }
  }

  mediaSource = new MediaSource();
  video.src = URL.createObjectURL(mediaSource);
  queue = [];

  mediaSource.addEventListener("sourceopen", () => {
    try {
      sourceBuffer = mediaSource.addSourceBuffer(
        'video/mp4; codecs="avc1.42E01E, mp4a.40.2"'
      );
    } catch (e) {
      console.error("addSourceBuffer error:", e);
      return;
    }

    sourceBuffer.mode = "segments";

    ws = new WebSocket(
      `ws://${
        window.location.host
      }/ws/video/?id=${videoId}&quality=${quality}&start=${Math.floor(
        currentTime
      )}`
    );

    ws.binaryType = "arraybuffer";

    ws.onmessage = (event) => {
      if (!sourceBuffer || mediaSource.readyState !== "open") return;
      const chunk = new Uint8Array(event.data);

      if (sourceBuffer.updating || queue.length > 0) {
        queue.push(chunk);
      } else {
        try {
          sourceBuffer.appendBuffer(chunk);
        } catch (e) {
          console.error("Append error:", e);
        }
      }
    };

    sourceBuffer.addEventListener("updateend", () => {
      if (queue.length > 0 && !sourceBuffer.updating) {
        sourceBuffer.appendBuffer(queue.shift());
      }
    });

    ws.onclose = () => console.log("WebSocket closed");
    ws.onerror = (err) => console.error("WebSocket error:", err);
  });

  video.addEventListener(
    "loadedmetadata",
    () => {
      if (!isNaN(currentTime)) video.currentTime = currentTime;
    },
    { once: true }
  );
}

// === Initial stream ===
startStream(qualitySelect.value);

// === Event listeners ===

// Play/Pause toggle
playPauseBtn.addEventListener("click", () => {
  if (video.paused) {
    video.play();
    playPauseBtn.textContent = "⏸";
  } else {
    video.pause();
    playPauseBtn.textContent = "▶";
  }
});

// Fullscreen toggle
fullscreenBtn.addEventListener("click", () => {
  if (!document.fullscreenElement) {
    video.parentElement.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
});

// Mute toggle
muteBtn.addEventListener("click", () => {
  video.muted = !video.muted;
  muteBtn.textContent = video.muted ? "🔇" : "🔊";
});

// Playback speed change
speedSelect.addEventListener("change", () => {
  video.playbackRate = parseFloat(speedSelect.value);
});

// Quality change triggers re-stream
qualitySelect.addEventListener("change", () => {
  startStream(qualitySelect.value);
});

// Seek on progress bar input
progressBar.addEventListener("input", () => {
  video.currentTime = (progressBar.value / 100) * duration;
});

// Auto-hide controls
let hideControlsTimeout;

function showControls() {
  controlsBar.classList.remove("opacity-0", "pointer-events-none");
  controlsBar.classList.add("opacity-100");
  clearTimeout(hideControlsTimeout);
  hideControlsTimeout = setTimeout(hideControls, 3000);
}

function hideControls() {
  controlsBar.classList.remove("opacity-100");
  controlsBar.classList.add("opacity-0", "pointer-events-none");
}

video.parentElement.addEventListener("mousemove", showControls);
video.parentElement.addEventListener("mouseleave", hideControls);
video.addEventListener("pause", () => (playPauseBtn.textContent = "▶"));
video.addEventListener("play", () => (playPauseBtn.textContent = "⏸"));

// Initial control display
showControls();
