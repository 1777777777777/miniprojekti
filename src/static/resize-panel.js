const folders = document.getElementById('folders');
const resizer = document.querySelector('.resizer');
const minWidth = 160;

function resizeFolders(width) {
    const maxWidth = Math.min(480, Math.max(minWidth, window.innerWidth - 320));
    const nextWidth = Math.min(maxWidth, Math.max(minWidth, Math.round(width)));
    folders.style.setProperty('--folder-width', `${nextWidth}px`);
    resizer.setAttribute('aria-valuemax', maxWidth);
    resizer.setAttribute('aria-valuenow', nextWidth);
}

resizer.addEventListener('pointerdown', (event) => {
    if (event.button !== 0) return;
    resizer.setPointerCapture(event.pointerId);
    resizer.classList.add('dragging');
});

resizer.addEventListener('pointermove', (event) => {
    if (!resizer.hasPointerCapture(event.pointerId)) return;
    resizeFolders(event.clientX - folders.getBoundingClientRect().left);
});

resizer.addEventListener('lostpointercapture', () => {
    resizer.classList.remove('dragging');
});

resizer.addEventListener('keydown', (event) => {
    const width = Number(resizer.getAttribute('aria-valuenow'));
    const widths = { ArrowLeft: width - 16, ArrowRight: width + 16, Home: minWidth, End: 480 };
    if (!Object.hasOwn(widths, event.key)) return;
    event.preventDefault();
    resizeFolders(widths[event.key]);
});

function fitFolders() {
    if (resizer.offsetWidth) resizeFolders(Number(resizer.getAttribute('aria-valuenow')));
}

window.addEventListener('resize', fitFolders);
fitFolders();
