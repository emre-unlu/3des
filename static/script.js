function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        const msg = document.getElementById('copy-msg');
        msg.style.display = 'block';
        msg.textContent = 'Copied to clipboard!';
        setTimeout(() => { msg.style.display = 'none'; }, 1500);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.copyable').forEach(function(elem) {
        elem.addEventListener('click', function() {
            copyToClipboard(this.textContent);
        });
    });

    const copyAll = document.getElementById('copy-all-btn');
    if (copyAll) {
        copyAll.addEventListener('click', function() {
            const texts = Array.from(document.querySelectorAll('.copyable'))
                              .map(el => el.textContent)
                              .join('\n');
            if (texts) {
                copyToClipboard(texts);
            }
        });
    }
});
