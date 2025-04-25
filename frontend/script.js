let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const statusText = document.getElementById("status");
const summaryDiv = document.getElementById("summaryResult");

recordBtn.onclick = async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);

  audioChunks = [];
  mediaRecorder.ondataavailable = e => {
    audioChunks.push(e.data);
  };

  mediaRecorder.onstart = () => {
    statusText.textContent = "Status: Recording...";
    recordBtn.disabled = true;
    stopBtn.disabled = false;
  };

  mediaRecorder.start();
};

stopBtn.onclick = async () => {
  mediaRecorder.stop();
  statusText.textContent = "Status: Processing...";
  recordBtn.disabled = false;
  stopBtn.disabled = true;

  mediaRecorder.onstop = async () => {
    const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
    const formData = new FormData();
    formData.append("audio", audioBlob);

    const res = await fetch("/summarize", {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    summaryDiv.innerHTML = `<h2>📝 Summary:</h2><p>${data.summary}</p>`;
    statusText.textContent = "Status: Done";
  };
};
