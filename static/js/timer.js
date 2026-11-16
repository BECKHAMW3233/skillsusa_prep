// Reusable countdown/stopwatch. targetMinutes <= 0 means "count up only" (no target).
function createDrillTimer(opts) {
  const clockEl = document.getElementById(opts.clockId);
  const statusEl = document.getElementById(opts.statusId);
  const overtimeEl = opts.overtimeId ? document.getElementById(opts.overtimeId) : null;
  const startBtn = opts.startBtnId ? document.getElementById(opts.startBtnId) : null;
  const resetBtn = opts.resetBtnId ? document.getElementById(opts.resetBtnId) : null;

  let running = false;
  let startTs = null;
  let elapsedMs = opts.initialElapsedMs || 0;
  let job = null;

  function targetSeconds() {
    return (opts.getTargetMinutes ? opts.getTargetMinutes() : 0) * 60;
  }

  function format(totalSeconds) {
    const m = Math.floor(totalSeconds / 60).toString().padStart(2, '0');
    const s = Math.floor(totalSeconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  function tick() {
    if (!running) return;
    elapsedMs = Date.now() - startTs;
    const elapsedSec = elapsedMs / 1000;
    clockEl.textContent = format(elapsedSec);

    const target = targetSeconds();
    if (target > 0) {
      if (elapsedSec > target) {
        const over = elapsedSec - target;
        if (overtimeEl) overtimeEl.textContent = `Over target by ${format(over)}`;
        statusEl.textContent = 'Over time!';
        statusEl.className = 'timer-status status-bad';
      } else {
        const remaining = target - elapsedSec;
        statusEl.textContent = `${format(remaining)} remaining`;
        statusEl.className = 'timer-status status-good';
        if (overtimeEl) overtimeEl.textContent = '';
      }
    } else {
      statusEl.textContent = 'Running...';
      statusEl.className = 'timer-status';
    }
    job = setTimeout(tick, 400);
  }

  function startStop() {
    if (!running) {
      running = true;
      startTs = Date.now() - elapsedMs;
      if (startBtn) { startBtn.textContent = 'Pause'; startBtn.className = 'btn orange'; }
      tick();
    } else {
      running = false;
      clearTimeout(job);
      if (startBtn) { startBtn.textContent = 'Resume'; startBtn.className = 'btn blue'; }
      statusEl.textContent = 'Paused';
      statusEl.className = 'timer-status';
    }
  }

  function reset() {
    running = false;
    clearTimeout(job);
    elapsedMs = 0;
    clockEl.textContent = '00:00';
    statusEl.textContent = 'Ready';
    statusEl.className = 'timer-status';
    if (overtimeEl) overtimeEl.textContent = '';
    if (startBtn) { startBtn.textContent = 'Start'; startBtn.className = 'btn green'; }
  }

  if (startBtn) startBtn.addEventListener('click', startStop);
  if (resetBtn) resetBtn.addEventListener('click', reset);

  return {
    getElapsedMinutes: () => Math.round(elapsedMs / 60000),
    start: () => { if (!running) startStop(); },
  };
}
