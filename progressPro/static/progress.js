const fileToDownload = 'kompyuter-busad_printer-xuvilagch-skanne.xlsx';
const startDownloadElem = document.getElementById('startDownload');
const downloadProgressElem = document.querySelector('.download-progress-bar_progress');

startDownloadElem.addEventListener('click', () => {
    console.log('Download Started');
    startDownloadElem.setAttribute('disabled', 'true');
    const dataChunks = [];
    fetch(fileToDownload)
        .then(response => {
            const reader = response.body.getReader();
            const totalSize = Number(response.headers.get('content-length'));
            let totalSizeDownloaded = 0;

            function readData() {
                return reader.read().then(result => {
                    if (result.value) {
                        dataChunks.push(result.value);
                        totalSizeDownloaded += result.value.length;
                        const percentage = Math.floor((totalSizeDownloaded / totalSize) * 100);

                        console.log(`${totalSizeDownloaded}/${totalSize} (${percentage}%)`);

                        downloadProgressElem.textContent = `${percentage}%`;
                        downloadProgressElem.style.width = `${percentage}%`;
                    }

                    if (!result.done) {
                        return readData();
                    }
                });
            }

            return readData();
        })
        .then(() => {
            console.log('Download finished');
            const downloadAnchor = document.createElement('a');
            const blob = new Blob(dataChunks);
            downloadAnchor.href = URL.createObjectURL(blob);
            downloadAnchor.download = fileToDownload.split('/').pop(); // Extract filename from URL
            document.body.appendChild(downloadAnchor);
            downloadAnchor.click();
            document.body.removeChild(downloadAnchor);
        })
        .catch(() => {
            downloadProgressElem.textContent = 'Download error';
            downloadProgressElem.classList.add('error');
        })
        .finally(() => {
            startDownloadElem.removeAttribute('disabled');
        });
});
