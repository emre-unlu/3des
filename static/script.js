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

function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
    const btn = document.getElementById('theme-toggle');
    if (btn) {
        btn.textContent = theme === 'dark' ? 'Switch to Light Mode' : 'Switch to Dark Mode';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(savedTheme || (prefersDark ? 'dark' : 'light'));

    const toggleBtn = document.getElementById('theme-toggle');
    if (toggleBtn) {
        toggleBtn.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            applyTheme(current === 'dark' ? 'light' : 'dark');
        });
    }

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

    const tooltip = document.getElementById('step-tooltip');
    document.querySelectorAll('.step-row').forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            if (tooltip) {
                tooltip.textContent = this.dataset.desc;
                const rect = this.getBoundingClientRect();
                tooltip.style.left = rect.left + window.scrollX + 'px';
                tooltip.style.top = rect.bottom + window.scrollY + 'px';
                tooltip.style.display = 'block';
            }
        });
        row.addEventListener('mouseleave', function() {
            if (tooltip) {
                tooltip.style.display = 'none';
            }
        });
    });
});
