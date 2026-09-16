let currentTab = 'ingredients';
let currentStepIdx = 0;
let timers = {};

function switchTab(tab) {
  currentTab = tab;
  document.getElementById('tab-ingredients').classList.toggle('active', tab === 'ingredients');
  document.getElementById('tab-cooking').classList.toggle('active', tab === 'cooking');
  
  document.getElementById('section-ingredients').style.display = tab === 'ingredients' ? 'block' : 'none';
  document.getElementById('section-cooking').style.display = tab === 'cooking' ? 'block' : 'none';
  
  const bottomBar = document.getElementById('bottom-bar');
  const topAppBar = document.querySelector('.top-app-bar');
  const viewTabs = document.querySelector('.view-mode-tabs');
  const videoCard = document.querySelector('.video-card');

  if (tab === 'cooking') {
    if (topAppBar) topAppBar.style.display = 'none';
    if (viewTabs) viewTabs.style.display = 'none';
    if (videoCard) videoCard.style.display = 'none';
    bottomBar.style.display = 'flex';
    renderStep(currentStepIdx);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  } else {
    if (topAppBar) topAppBar.style.display = 'flex';
    if (viewTabs) viewTabs.style.display = 'flex';
    if (videoCard) videoCard.style.display = 'block';
    bottomBar.style.display = 'none';
  }
}

function toggleIngredient(card) {
  card.classList.toggle('checked');
  const checkbox = card.querySelector('.custom-checkbox');
  if (card.classList.contains('checked')) {
    checkbox.innerHTML = '✓';
  } else {
    checkbox.innerHTML = '';
  }
}

function renderStep(idx) {
  const steps = document.querySelectorAll('.cook-step-card-wrapper');
  if (idx < 0) idx = 0;
  if (idx >= steps.length) idx = steps.length - 1;
  currentStepIdx = idx;

  steps.forEach((step, i) => {
    step.style.display = i === idx ? 'block' : 'none';
  });

  const progressFill = document.getElementById('step-progress');
  if (progressFill) {
    const pct = ((idx + 1) / steps.length) * 100;
    progressFill.style.width = `${pct}%`;
  }

  const btnPrev = document.getElementById('btn-prev');
  if (btnPrev) {
    btnPrev.disabled = idx === 0;
    btnPrev.style.opacity = idx === 0 ? '0.4' : '1';
  }

  const btnNext = document.getElementById('btn-next');
  if (btnNext) {
    if (idx === steps.length - 1) {
      btnNext.innerHTML = '🎉 Selesai!';
      btnNext.style.background = 'var(--md-sys-color-tertiary)';
      btnNext.style.color = 'var(--md-sys-color-on-tertiary)';
    } else {
      btnNext.innerHTML = 'Langkah Berikutnya ➔';
      btnNext.style.background = 'var(--md-sys-color-primary)';
      btnNext.style.color = 'var(--md-sys-color-on-primary)';
    }
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function nextStep() {
  const steps = document.querySelectorAll('.cook-step-card-wrapper');
  if (currentStepIdx < steps.length - 1) {
    renderStep(currentStepIdx + 1);
  } else {
    alert('Selamat! Masakan Egg Chicken Roll sudah selesai dibuat!');
  }
}

function prevStep() {
  if (currentStepIdx > 0) {
    renderStep(currentStepIdx - 1);
  }
}

// Timer Logic
function startTimer(id, initialSeconds) {
  const btn = document.getElementById(`btn-timer-${id}`);
  const display = document.getElementById(`display-timer-${id}`);
  
  if (timers[id] && timers[id].interval) {
    // Pause / Stop
    clearInterval(timers[id].interval);
    timers[id].interval = null;
    btn.innerHTML = '▶ Mulai';
    return;
  }

  if (!timers[id]) {
    timers[id] = { remaining: initialSeconds, interval: null };
  }

  btn.innerHTML = '⏸ Jeda';
  
  timers[id].interval = setInterval(() => {
    timers[id].remaining--;
    const mins = Math.floor(timers[id].remaining / 60);
    const secs = timers[id].remaining % 60;
    display.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    
    if (timers[id].remaining <= 0) {
      clearInterval(timers[id].interval);
      timers[id].interval = null;
      btn.innerHTML = 'Selesai!';
      btn.style.background = 'var(--md-sys-color-primary)';
      display.textContent = '00:00 - WAKTU HABIS!';
      if ('vibrate' in navigator) navigator.vibrate([300, 100, 300]);
    }
  }, 1000);
}

// Swipe gestures for one-handed cooking
let touchStartX = 0;
let touchEndX = 0;

// Head Tilt Detection (MediaPipe Face Mesh + Math Roll Angle)
let cameraStream = null;
let isCameraActive = false;
let gestureCooldown = false;
let faceMesh = null;
let mpCamera = null;

async function toggleCameraGesture() {
  const sensorBtn = document.getElementById('sensor-pill');
  const sensorIcon = document.getElementById('sensor-pill-icon');
  let video = document.getElementById('webcam');

  if (isCameraActive) {
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }
    isCameraActive = false;
    sensorBtn.classList.remove('active');
    sensorIcon.innerText = '🗣️';
    return;
  }

  try {
    sensorIcon.innerText = '⏳';
    
    if (!video) {
      video = document.createElement('video');
      video.id = 'webcam';
      video.setAttribute('autoplay', '');
      video.setAttribute('playsinline', '');
      video.setAttribute('muted', '');
      video.style.cssText = 'position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none;';
      document.body.appendChild(video);
    }

    if (!faceMesh) {
      faceMesh = new FaceMesh({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/face_mesh/${file}`
      });

      faceMesh.setOptions({
        maxNumFaces: 1,
        refineLandmarks: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
      });

      faceMesh.onResults(onFaceResults);
    }

    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 320 }, height: { ideal: 240 } },
      audio: false
    });
    
    cameraStream = stream;
    video.srcObject = stream;
    await video.play();

    isCameraActive = true;
    sensorBtn.classList.add('active');
    sensorIcon.innerText = '🟢';

    // Process frames directly with requestAnimationFrame
    async function processVideoFrame() {
      if (!isCameraActive) return;
      if (video.readyState >= 2) {
        await faceMesh.send({ image: video });
      }
      animationFrameId = requestAnimationFrame(processVideoFrame);
    }
    animationFrameId = requestAnimationFrame(processVideoFrame);

  } catch (err) {
    console.error('Camera/MediaPipe error:', err);
    alert('Izin kamera diperlukan untuk sensor miring kepala di browser Safari/Chrome.');
    sensorBtn.classList.remove('active');
    sensorIcon.innerText = '🗣️';
  }
}

let baselineBrowDist = null;

function onFaceResults(results) {
  if (gestureCooldown || !results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
    return;
  }

  const landmarks = results.multiFaceLandmarks[0];
  const leftEye = landmarks[33];
  const rightEye = landmarks[263];
  
  // MediaPipe FaceMesh canonical landmark indices:
  // Left eyebrow middle = 105, Right eyebrow middle = 334
  // Left eye center top = 159, Right eye center top = 386
  // Nose bridge / between eyes = 168
  const leftEyebrow = landmarks[105];
  const rightEyebrow = landmarks[334];
  const leftEyeTop = landmarks[159];
  const rightEyeTop = landmarks[386];

  if (!leftEye || !rightEye) return;

  // 1. Detect Eyebrow Raise (Adaptive delta relative to neutral face)
  if (leftEyebrow && rightEyebrow && leftEyeTop && rightEyeTop) {
    const leftDist = leftEyeTop.y - leftEyebrow.y;
    const rightDist = rightEyeTop.y - rightEyebrow.y;
    const eyeSpan = Math.hypot(rightEye.x - leftEye.x, rightEye.y - leftEye.y);
    const currentRatio = ((leftDist + rightDist) / 2) / (eyeSpan || 1);

    // Exponential moving average for baseline face calibration
    if (baselineBrowDist === null) {
      baselineBrowDist = currentRatio;
    } else {
      // Slowly adapt baseline when face is relaxed
      if (currentRatio < baselineBrowDist * 1.1) {
        baselineBrowDist = baselineBrowDist * 0.95 + currentRatio * 0.05;
      }
    }

    // Trigger when eyebrows lift > 15% above baseline or absolute ratio > 0.20
    if (currentRatio > baselineBrowDist * 1.18 || currentRatio > 0.21) {
      triggerEyebrowGesture();
      return;
    }
  }

  // 2. Detect Head Tilt (Next / Prev Step)
  const dy = rightEye.y - leftEye.y;
  const dx = rightEye.x - leftEye.x;
  const angleRad = Math.atan2(dy, dx);
  const angleDeg = angleRad * (180 / Math.PI);

  // Threshold: ±10° tilt
  if (angleDeg < -10) {
    triggerHeadGesture('next');
  } else if (angleDeg > 10) {
    triggerHeadGesture('prev');
  }
}

function triggerEyebrowGesture() {
  gestureCooldown = true;
  const sensorIcon = document.getElementById('sensor-pill-icon');
  if (sensorIcon) {
    sensorIcon.innerText = '🤨';
  }

  // Find timer on currently active step card
  const activeStepWrapper = document.getElementById(`step-wrapper-${currentStepIdx}`);
  if (activeStepWrapper) {
    const timerBtn = activeStepWrapper.querySelector('.btn-timer');
    if (timerBtn) {
      timerBtn.click();
      if ('vibrate' in navigator) navigator.vibrate([150]);
    }
  }

  setTimeout(() => {
    gestureCooldown = false;
    if (sensorIcon && isCameraActive) {
      sensorIcon.innerText = '🟢';
    }
  }, 1200);
}

function triggerHeadGesture(direction) {
  gestureCooldown = true;
  const sensorIcon = document.getElementById('sensor-pill-icon');
  if (sensorIcon) {
    sensorIcon.innerText = direction === 'next' ? '👉' : '👈';
  }

  if (direction === 'next') {
    nextStep();
  } else if (direction === 'prev') {
    prevStep();
  }

  // Cooldown 1.5s so user can straighten head back without double-trigger
  setTimeout(() => {
    gestureCooldown = false;
    if (sensorIcon && isCameraActive) {
      sensorIcon.innerText = '🟢';
    }
  }, 1500);
}

document.addEventListener('DOMContentLoaded', () => {
  const cookSection = document.getElementById('section-cooking');
  cookSection.addEventListener('touchstart', e => {
    touchStartX = e.changedTouches[0].screenX;
  }, false);

  cookSection.addEventListener('touchend', e => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  }, false);

  function handleSwipe() {
    if (currentTab !== 'cooking') return;
    if (touchEndX < touchStartX - 50) {
      nextStep(); // Swipe left -> Next
    }
    if (touchEndX > touchStartX + 50) {
      prevStep(); // Swipe right -> Prev
    }
  }
});
