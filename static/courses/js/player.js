const video = document.getElementById("video");
const qualitySelect = document.getElementById("qualitySelect");
const durationDisplay = document.getElementById("durationDisplay");
const speedSelect = document.getElementById("speedSelect");
const muteBtn = document.getElementById("muteBtn");

let mediaSource = new MediaSource();
let sourceBuffer;
let ws;
let queue = [];
let currentTime = 0;
let totalDuration = video.duration;

video.src = URL.createObjectURL(mediaSource);

// Format time as mm:ss
function formatTime(seconds) {
  const min = Math.floor(seconds / 60)
    .toString()
    .padStart(2, "0");
  const sec = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${min}:${sec}`;
}

// Update duration display
function updateDuration() {
  const current = formatTime(video.currentTime || 0);
  const total = formatTime(totalDuration || video.duration || 0);
  durationDisplay.textContent = `${current} / ${total}`;
}

video.addEventListener("loadedmetadata", () => {
  totalDuration = video.duration;
});
video.addEventListener("timeupdate", updateDuration);

// Stream video over WebSocket
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

// Quality selector change event
qualitySelect.addEventListener("change", () => {
  startStream(qualitySelect.value);
});

// Playback speed selector
speedSelect.addEventListener("change", () => {
  video.playbackRate = parseFloat(speedSelect.value);
});

startStream(qualitySelect.value);
