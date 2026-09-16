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
  if (tab === 'cooking') {
    bottomBar.style.display = 'flex';
    renderStep(currentStepIdx);
  } else {
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

  window.scrollTo({ top: document.getElementById('section-cooking').offsetTop - 80, behavior: 'smooth' });
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

// Camera Vision Hand Wave Detection
let cameraStream = null;
let isCameraActive = false;
let animationFrameId = null;
let lastFrameData = null;
let gestureCooldown = false;

async function toggleCameraGesture() {
  const btn = document.getElementById('btn-toggle-cam');
  const video = document.getElementById('webcam');
  const status = document.getElementById('cam-status');

  if (isCameraActive) {
    // Stop camera
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => track.stop());
    }
    if (animationFrameId) cancelAnimationFrame(animationFrameId);
    isCameraActive = false;
    btn.innerHTML = '📷 Aktifkan Kamera';
    btn.style.background = 'var(--md-sys-color-primary-container)';
    btn.style.color = 'var(--md-sys-color-on-primary-container)';
    status.innerText = 'Gunakan kamera depan tanpa menyentuh layar';
    return;
  }

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'user', width: { ideal: 320 }, height: { ideal: 240 } },
      audio: false
    });
    cameraStream = stream;
    video.srcObject = stream;
    await video.play();
    isCameraActive = true;
    btn.innerHTML = '🛑 Matikan Kamera';
    btn.style.background = 'var(--md-sys-color-error, #ba1a1a)';
    btn.style.color = '#ffffff';
    status.innerText = 'Aktif: Lambaikan tangan ke KIRI (Berikutnya) / KANAN (Balik)';

    startMotionDetection();
  } catch (err) {
    console.error('Camera access error:', err);
    alert('Izin kamera diperlukan untuk fitur lambaian tangan. Pastikan mengizinkan akses kamera di browser iPhone Safari/Chrome.');
  }
}

function startMotionDetection() {
  const video = document.getElementById('webcam');
  const canvas = document.getElementById('motion-canvas');
  const ctx = canvas.getContext('2d', { willReadFrequently: true });
  const indicator = document.getElementById('gesture-indicator');

  const width = canvas.width;
  const height = canvas.height;

  function processFrame() {
    if (!isCameraActive) return;

    if (video.readyState === video.HAVE_ENOUGH_DATA) {
      ctx.drawImage(video, 0, 0, width, height);
      const frame = ctx.getImageData(0, 0, width, height);

      if (lastFrameData && !gestureCooldown) {
        let leftMotion = 0;
        let rightMotion = 0;
        const threshold = 30; // pixel intensity delta threshold

        // Split viewport horizontally into Left and Right zones
        const halfWidth = Math.floor(width / 2);

        for (let y = 0; y < height; y += 4) {
          for (let x = 0; x < width; x += 4) {
            const idx = (y * width + x) * 4;
            // Greyscale difference
            const diff = Math.abs(frame.data[idx] - lastFrameData.data[idx]) +
                         Math.abs(frame.data[idx+1] - lastFrameData.data[idx+1]) +
                         Math.abs(frame.data[idx+2] - lastFrameData.data[idx+2]);

            if (diff > threshold * 3) {
              if (x < halfWidth) {
                // In mirrored camera: left in image is right in real life
                leftMotion++;
              } else {
                rightMotion++;
              }
            }
          }
        }

        const totalPixels = (width / 4) * (height / 4);
        const leftRatio = leftMotion / totalPixels;
        const rightRatio = rightMotion / totalPixels;
        const triggerThreshold = 0.08; // 8% pixel movement in zone

        // Mirror handling:
        // User moves hand to LEFT -> Camera sensor sees motion on left zone (mirrored)
        // User moves hand to RIGHT -> Camera sensor sees motion on right zone (mirrored)
        if (leftRatio > triggerThreshold && leftRatio > rightRatio * 1.5) {
          triggerGesture('next', '👉 Gerakan Terdeteksi: Langkah Berikutnya!');
        } else if (rightRatio > triggerThreshold && rightRatio > leftRatio * 1.5) {
          triggerGesture('prev', '👈 Gerakan Terdeteksi: Langkah Sebelumnya!');
        }
      }

      lastFrameData = frame;
    }

    animationFrameId = requestAnimationFrame(processFrame);
  }

  function triggerGesture(direction, text) {
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

    // Cooldown 1.5 seconds to avoid double triggering
    setTimeout(() => {
      gestureCooldown = false;
      if (status) {
        status.innerText = 'Aktif: Lambaikan tangan ke KIRI (Berikutnya) / KANAN (Balik)';
        status.style.color = 'var(--md-sys-color-on-surface-variant)';
        status.style.fontWeight = 'normal';
      }
    }, 1500);
  }

  animationFrameId = requestAnimationFrame(processFrame);
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
