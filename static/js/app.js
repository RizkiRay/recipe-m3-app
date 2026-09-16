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

  if (tab === 'cooking') {
    if (topAppBar) topAppBar.style.display = 'none';
    bottomBar.style.display = 'flex';
    renderStep(currentStepIdx);
  } else {
    if (topAppBar) topAppBar.style.display = 'flex';
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

  window.scrollTo({ top: document.getElementById('section-cooking').offsetTop - 10, behavior: 'smooth' });
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
  const btn = document.getElementById('btn-toggle-cam');
  const video = document.getElementById('webcam');
  const status = document.getElementById('cam-status');

  if (isCameraActive) {
    if (mpCamera) {
      mpCamera.stop();
    }
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }
    isCameraActive = false;
    btn.innerHTML = '📷 Aktifkan Sensor';
    btn.style.background = 'var(--md-sys-color-primary-container)';
    btn.style.color = 'var(--md-sys-color-on-primary-container)';
    status.innerText = 'Miringkan kepala 45°: Kanan (Berikutnya) / Kiri (Sebelumnya)';
    return;
  }

  try {
    btn.innerHTML = '⏳ Menyiapkan AI...';
    
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

    mpCamera = new Camera(video, {
      onFrame: async () => {
        if (isCameraActive) {
          await faceMesh.send({ image: video });
        }
      },
      width: 320,
      height: 240,
      facingMode: 'user'
    });

    await mpCamera.start();
    isCameraActive = true;
    btn.innerHTML = '🛑 Matikan Sensor';
    btn.style.background = 'var(--md-sys-color-error, #ba1a1a)';
    btn.style.color = '#ffffff';
    status.innerText = 'Sensor Aktif: Miringkan kepala ±45° ke Kiri / Kanan';
  } catch (err) {
    console.error('Camera/MediaPipe error:', err);
    alert('Izin kamera diperlukan untuk sensor miring kepala di browser.');
    btn.innerHTML = '📷 Aktifkan Sensor';
  }
}

function onFaceResults(results) {
  if (gestureCooldown || !results.multiFaceLandmarks || results.multiFaceLandmarks.length === 0) {
    return;
  }

  const landmarks = results.multiFaceLandmarks[0];
  
  // Landmark 33 = outer corner left eye, Landmark 263 = outer corner right eye
  // Landmark 10 = top of forehead, Landmark 152 = chin
  const leftEye = landmarks[33];
  const rightEye = landmarks[263];
  const forehead = landmarks[10];
  const chin = landmarks[152];

  if (!leftEye || !rightEye || !forehead || !chin) return;

  // Calculate eye slope angle in degrees
  const dy = rightEye.y - leftEye.y;
  const dx = rightEye.x - leftEye.x;
  
  // Angle in radians then convert to degrees (-180 to 180)
  const angleRad = Math.atan2(dy, dx);
  const angleDeg = angleRad * (180 / Math.PI);

  const status = document.getElementById('cam-status');
  
  // Threshold: ±18° to 20° tilt (natural, slight head tilt)
  if (angleDeg < -18) {
    // Tilted right
    triggerHeadGesture('next', '👉 Kepala Miring Kanan: Langkah Berikutnya!');
  } else if (angleDeg > 18) {
    // Tilted left
    triggerHeadGesture('prev', '👈 Kepala Miring Kiri: Langkah Sebelumnya!');
  }
}

function triggerHeadGesture(direction, text) {
  gestureCooldown = true;
  const status = document.getElementById('cam-status');
  if (status) {
    status.innerText = text;
    status.style.color = 'var(--md-sys-color-primary)';
    status.style.fontWeight = 'bold';
  }

  if (direction === 'next') {
    nextStep();
  } else if (direction === 'prev') {
    prevStep();
  }

  // Cooldown 1.5s so user can straighten head back without double-trigger
  setTimeout(() => {
    gestureCooldown = false;
    if (status) {
      status.innerText = 'Sensor Aktif: Miringkan kepala ±45° ke Kiri / Kanan';
      status.style.color = 'var(--md-sys-color-on-surface-variant)';
      status.style.fontWeight = 'normal';
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
