// Both parts are enhancements: without JS the page reads the same and each
// thumbnail opens its full-size snapshot.

// The latest release, from the same endpoint as the game's own update check.
fetch('https://api.github.com/repos/L4w1i3t/Enter-M/releases/latest')
  .then((response) => (response.ok ? response.json() : null))
  .then((release) => {
    if (!release) return;
    const date = new Date(release.published_at).toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric',
    });
    document.getElementById('release').textContent = ` Latest release: ${release.tag_name}, ${date}.`;
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
