import cv2
import os

def extract_first_frame(video_path):
    """
    Extract the first frame from a video file and save it as an image.

    Parameters:
    video_path (str): The path of the video file.

    """
    directory, filename = os.path.split(video_path)
    name, _ = os.path.splitext(filename)
    capture = cv2.VideoCapture(video_path)
    success, image = capture.read()
    if success:
        cv2.imwrite(os.path.join(directory, f"{name}.jpg"), image)


async def process_photo(photo, new_date):
    """
    Process and download a photo from iCloud.

    Parameters:
    photo (obj): The photo object to download.
    new_date (datetime): The date for naming the downloaded file.
    """
    date_string = f"{new_date.year}-{new_date.month}-{new_date.day}"

    if not os.path.exists(date_string):
        os.makedirs(date_string)

    extension = photo.versions['original']['filename'].split(".")[1]
    filename = f"{date_string}/{new_date.month}-{new_date.day}-{new_date.year}-{new_date.hour}-{new_date.minute}-{new_date.second}-{new_date.microsecond}.{extension}"

    if "heic" in photo.filename.lower():
        download = photo.download('medium')
        video_name = filename.replace('.HEIC', '.mov')
        with open(video_name, 'wb') as file:
            file.write(download.raw.read())
        extract_first_frame(video_name)
    else:
        download = photo.download('original')
        with open(filename, 'wb') as file:
            file.write(download.raw.read())