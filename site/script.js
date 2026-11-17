// Every part is an enhancement: without JS the card's plates are plain links,
// and each thumbnail opens its full-size snapshot.

// The title card: the row under the pointer or the keyboard fills the note
// and the tick, and the orrery answers it, as on the title screen.
const hero = document.querySelector('.hero');
const card = hero.querySelector('.card');
const rows = [...card.querySelectorAll('.rows .plate')];
const noteText = document.getElementById('note-text');
const noteKey = document.getElementById('note-key');
const tick = document.getElementById('tick');
const stage = hero.querySelector('.stage');
const core = hero.querySelector('.core');
const still = matchMedia('(prefers-reduced-motion: reduce)');
const restNote = noteText.textContent;
let selected = null;

function select(index) {
  const row = rows[index];
  const changed = (row ? index : null) !== selected;
  selected = row ? index : null;
  const num = String(index + 1).padStart(2, '0');
  noteText.textContent = row ? row.dataset.note : restNote;
  noteKey.textContent = row ? `${row.dataset.tag} / ${num}` : '';
  tick.textContent = row ? `[${num}] ${row.dataset.tag}` : '';
  tick.classList.toggle('on', !!row);
  if (row) {
    const h = hero.getBoundingClientRect();
    const r = row.getBoundingClientRect();
    const z = parseFloat(getComputedStyle(tick).zoom) || 1;  // a zoomed tick scales its own top/left
    tick.style.top = `${(r.top + r.height / 2 - h.top) / z}px`;
    tick.style.left = `${(card.getBoundingClientRect().right - h.left + 4) / z}px`;
  }
  if (still.matches) return;
  stage.style.setProperty('--months', `${15 * (selected ?? 0)}deg`);
  stage.style.setProperty('--days', `${-6 * (selected ?? 0)}deg`);
  if (row && changed) {
    core.classList.remove('pulse');
    void core.offsetWidth;  // restart the flare
    core.classList.add('pulse');
  }
}

rows.forEach((row, i) => {
  row.addEventListener('pointerenter', () => select(i));
  row.addEventListener('focus', () => select(i));
});
// Leaving falls back to a keyboard-focused row, else to the rest note.
card.querySelector('.rows').addEventListener('pointerleave', () => {
  const i = rows.findIndex((r) => r.matches(':focus-visible'));
  select(i >= 0 ? i : null);
});
card.addEventListener('focusout', (event) => {
  if (!card.contains(event.relatedTarget)) select(null);
});

// The latest release, from the same endpoint as the game's own update check.
fetch('https://api.github.com/repos/L4w1i3t/Enter-M/releases/latest')
  .then((response) => (response.ok ? response.json() : null))
  .then((release) => {
    if (!release?.tag_name) return;
    const tag = `v${release.tag_name.replace(/^v/, '')}`;
    const date = new Date(release.published_at).toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric',
    });
    document.getElementById('readout').textContent = `${tag} // LINK STABLE`;
    rows[0].dataset.note += ` Latest release: ${tag}, ${date}.`;
    if (selected === 0) select(0);
  })
  .catch(() => {});

// Snapshots: the strip picks what the big print shows.
const strip = document.querySelector('.strip');
const shots = [...strip.querySelectorAll('a')];
const view = document.getElementById('view-img');
const count = document.getElementById('view-count');
const glide = matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
let current = 0;

function show(index) {
  current = (index + shots.length) % shots.length;
  const shot = shots[current];
  if (view.getAttribute('src') !== shot.getAttribute('href')) {
    view.classList.add('loading');
    view.src = shot.getAttribute('href');
  }
  view.alt = shot.querySelector('img').alt;
  count.textContent = `${current + 1} / ${shots.length}`;
  shots.forEach((s, i) => s.setAttribute('aria-current', String(i === current)));
  // Scroll the strip itself, never the page.
  const item = shot.parentElement;
  strip.scrollTo({ left: item.offsetLeft - (strip.clientWidth - item.offsetWidth) / 2, behavior: glide });
}

view.addEventListener('load', () => view.classList.remove('loading'));

strip.addEventListener('click', (event) => {
  const shot = event.target.closest('a');
  if (!shot) return;
  event.preventDefault();
  show(shots.indexOf(shot));
});

for (const [selector, step] of [['.prev', -1], ['.next', 1]]) {
  const button = document.querySelector(selector);
  button.hidden = false;
  button.addEventListener('click', () => show(current + step));
}

document.querySelector('.snapshots').addEventListener('keydown', (event) => {
  const step = { ArrowLeft: -1, ArrowRight: 1 }[event.key];
  if (!step) return;
  event.preventDefault();
  show(current + step);
  if (shots.includes(document.activeElement)) shots[current].focus();
});

show(0);
