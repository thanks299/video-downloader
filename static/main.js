document.getElementById('downloadBtn').addEventListener('click', async function (e) {
    e.preventDefault();
    const videoUrl = document.getElementById('videoUrl').value;
    const format = document.getElementById('format').value;

    await download(videoUrl, format);

});
const link = document.getElementById("downloadLink");

link.classList.add("hidden");
const download = async (videoUrl, format) => {

    const opts = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: videoUrl, format: format }),
    }

    try {
        const response = await fetch('/download-video', opts);
        const data = await response.json();
        console.log(data);

        await getVideo(data.task_id);
    }
    catch (e) {
	    console.error('Error during video download:', e);
    }
}

const getVideo = async (id) => {
    try {
        const res = await fetch(`/status/${id}`);  // Check the status of the download
        if (res.ok) {
            const fileBlob = await res.blob();  // Get the file blob
            link.href = URL.createObjectURL(fileBlob);  // Create an object URL for the blob

            // Show the download link by removing the hidden class
            link.classList.remove('hidden');

            // filename for the download
            link.download = "Click to save file";

            console.log('File ready for download');
        } else {
            console.error('Failed to retrieve video');
        }
    } catch (e) {
        console.error('Error fetching video status:', e);
    }
}
