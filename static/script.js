function showMessage(text) {
    const msg = document.getElementById('copy-msg');
    if (msg) {
        msg.style.display = 'block';
        msg.textContent = text;
        setTimeout(() => { msg.style.display = 'none'; }, 1500);
    }
}

function copyToClipboard(text, message) {
    navigator.clipboard.writeText(text).then(function() {
        showMessage(message || 'Copied to clipboard!');
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
            const ciphertextEl = document.getElementById('ciphertext-result');
            const keyEl = document.getElementById('key-result');
            const ivEl = document.getElementById('iv-result');

            const cInput = document.getElementById('ciphertext-input');
            const kInput = document.getElementById('key-input');
            const ivInput = document.getElementById('iv-input');

            const pieces = [];

            if (ciphertextEl) {
                pieces.push(ciphertextEl.textContent);
                if (cInput) cInput.value = ciphertextEl.textContent;
            }
            if (keyEl) {
                pieces.push(keyEl.textContent);
                if (kInput) kInput.value = keyEl.textContent;
            }
            if (ivEl) {
                pieces.push(ivEl.textContent);
                if (ivInput) ivInput.value = ivEl.textContent;
            }

            if (pieces.length) {
                copyToClipboard(pieces.join('\n'), 'Values copied & filled below!');
            }
        });
    }
});
