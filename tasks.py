from celery import Celery
import yt_dlp
import uuid

# Create Celery instance
celery_app = Celery('tasks',
                    broker='redis://localhost:6379/0',
                    backend='redis://localhost:6379/0')

# Define the video downloading task


@celery_app.task(bind=True)
def download_video_task(self, url, format_choice):
    try:  # Ensure you have a try block here
        # Desired custom file name with the extension placeholder
        # new_file_name = f"file{uuid.uuid4()}.%(ext)s"
        new_file_name = '%(id)s.%(ext)s'

        ydl_opts = {
            # Save to 'downloads' folder with the new file name
            'outtmpl': f'downloads/{new_file_name}',
            'format': format_choice  # Format chosen by the user
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info_dict)

        return file_name
    except Exception as e:  # Correctly placed except block
        # Handle the error appropriately
        return str(e)
