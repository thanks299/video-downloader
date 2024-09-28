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

    }
}

const getVideo = async (id) => {
    const res = await fetch(`/status/${id}`);



    if (res.ok) {
        const fileBlob = await res.blob();
        link.href = URL.createObjectURL(fileBlob);


        link.classList.toggle('hidden')
        console.log(link)// Specify the file name for download
        // link.click();  // Simulate click to download the file
        // document.body.removeChild(link);
    }

}
