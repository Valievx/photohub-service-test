const photoSocket = new WebSocket(
    'ws://' + window.location.host + '/ws/photo-process/'
);

photoSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'photo_update') {
        const existingCard = document.querySelector(`[data-photo-id="${data.data.id}"]`);
        updatePhotoCard(data.data);

        document.querySelector('.badge.bg-primary').textContent = `Total: ${data.data.stats.total}`;
        document.querySelector('.badge.bg-success').textContent = `Completed: ${data.data.stats.completed}`;
        document.querySelector('.badge.bg-warning').textContent = `Pending: ${data.data.stats.pending}`;
    }
};

function formatDate(date) {
    const options = {
        day: '2-digit',
        month: 'short',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    };

    return date.toLocaleDateString('ru-RU', options)
        .replace(/ г\./, '')
        .replace(/\./g, '')
        .replace(/\,/g, '')
        .replace(/(\d+) (\D+) (\d+)/, (_, day, month, year) => {
            return `${day} ${month.charAt(0).toUpperCase() + month.slice(1)} ${year}`;
        });
}

function updatePhotoCard(data) {
    const photoCard = document.querySelector(`[data-photo-id="${data.id}"]`);
    if (!photoCard) {
        let statusIcon;
        if (data.status === 'completed') {
            statusIcon = '<i class="bi bi-check-circle text-success"></i>';
        } else if (data.status === 'processing') {
            statusIcon = '<i class="bi bi-gear text-info spin"></i>';
        } else if (data.status === 'pending') {
            statusIcon = '<i class="bi bi-hourglass-split text-warning spin"></i>';
        } else {
            statusIcon = '<i class="bi bi-x-circle text-danger"></i>';
        }

        const resultsDiv = document.getElementById('results');
        const newCard = document.createElement('div');
        newCard.className = 'list-group-item list-group-item-custom';
        newCard.dataset.photoId = data.id;
        newCard.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <h5 class="mb-1">${data.filename}</h5>
                    <small>${formatDate(new Date(data.uploaded_at))}</small>
                </div>
                <div>
                    <span class="mb-1 number-badge">Number: ${data.number || '-'}</span>
                    <span class="status-badge">${statusIcon}</span>
                </div>
            </div>
        `;
        resultsDiv.insertBefore(newCard, resultsDiv.firstChild);
    } else {
        const statusBadge = photoCard.querySelector('.status-badge');
        let statusIcon;
        if (data.status === 'completed') {
            statusIcon = '<i class="bi bi-check-circle text-success"></i>';
        } else if (data.status === 'processing') {
            statusIcon = '<i class="bi bi-gear text-info spin"></i>';
        } else if (data.status === 'pending') {
            statusIcon = '<i class="bi bi-hourglass-split text-warning spin"></i>';
        } else {
            statusIcon = '<i class="bi bi-x-circle text-danger"></i>';
        }
        statusBadge.innerHTML = statusIcon;
        const numberBadge = photoCard.querySelector('.number-badge');
        if (numberBadge) {
            numberBadge.textContent = `Number: ${data.number || '-'}`;
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function uploadImage() {
    const startTime = performance.now();
    const fileInput = document.getElementById('imageInput');
    const statusElement = document.getElementById('singleUploadTime');
    const massProgress = document.getElementById('massUploadProgress');

    massProgress.style.display = 'none';
    statusElement.style.display = 'block';
    statusElement.innerHTML = 'Status: <span class="text-warning">Uploading...</span>';

    if (!fileInput.files[0]) {
        statusElement.innerHTML = 'Status: <span class="text-danger">No file selected!</span>';
        return;
    }

    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    const csrftoken = getCookie('csrftoken');

    try {
        const response = await fetch('/api/photohub/process/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        });

        const uploadTime = ((performance.now() - startTime)/1000).toFixed(2);

        if (response.ok) {
            const data = await response.json();
            statusElement.innerHTML = `Status: <span class="text-success">Upload successful (${uploadTime}s)</span>`;
        } else {
            statusElement.innerHTML = `Status: <span class="text-danger">Error ${response.status}</span>`;
        }
    } catch (error) {
        statusElement.innerHTML = `Status: <span class="text-danger">${error.message}</span>`;
        console.error('Error:', error);
    }
}

async function massUpload() {
    const startTime = performance.now();
    const fileInput = document.getElementById('imageInput');
    const massProgress = document.getElementById('massUploadProgress');
    const statusElement = document.getElementById('singleUploadTime');

    statusElement.style.display = 'none';
    massProgress.style.display = 'block';

    const progressBar = massProgress.querySelector('.progress-bar-custom');
    const processedCount = document.getElementById('processedCount');
    const massTimeElement = document.getElementById('massUploadTime');

    if (!fileInput.files[0]) {
        alert('Please select a file first');
        return;
    }

    if (!confirm('This will upload the file 100 times. Continue?')) return;

    progressBar.style.width = '0%';
    progressBar.style.backgroundColor = '#4CAF50';
    processedCount.textContent = '0';
    massTimeElement.textContent = '0';

    const csrftoken = getCookie('csrftoken');
    const CONCURRENCY = 20;
    const TOTAL_REQUESTS = 100;
    let completed = 0;
    const errors = [];

    const requests = Array.from({ length: TOTAL_REQUESTS }, (_, i) => async () => {
        const formData = new FormData();
        formData.append('image', fileInput.files[0]);

        try {
            await fetch('/api/photohub/process/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            });
        } catch (error) {
            errors.push({ attempt: i + 1, error: error.message });
        } finally {
            completed++;
            const progress = (completed / TOTAL_REQUESTS) * 100;
            const elapsed = ((performance.now() - startTime)/1000).toFixed(1);

            processedCount.textContent = completed;
            massTimeElement.textContent = elapsed;
            progressBar.style.width = `${progress}%`;
        }
    });

    const pool = [];
    for (const request of requests) {
        const promise = request();
        pool.push(promise);

        if (pool.length >= CONCURRENCY) {
            await Promise.race(pool);
        }
    }

    await Promise.all(pool);

    const totalTime = ((performance.now() - startTime)/1000).toFixed(1);
    progressBar.style.backgroundColor = errors.length > 0 ? '#ff4444' : '#4CAF50';
    massTimeElement.textContent = totalTime;

    if (errors.length > 0) {
        console.error('Errors during mass upload:', errors);
        alert(`Completed with ${errors.length} errors. Check console for details.`);
    }
}