import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS


def get_photo_taken_date(file_path):
    try:
        image = Image.open(file_path)
        exif_data = image._getexif()

        if exif_data:
            for tag_id, value in exif_data.items():
                tag = TAGS.get(tag_id, tag_id)

                if tag == "DateTimeOriginal":
                    # Format: 'YYYY:MM:DD HH:MM:SS'
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")

    except Exception:
        pass

    return None


def organize_photos_by_year(source_folder, destination_folder):
    image_extensions = ('.jpg', '.jpeg')

    for file in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file)

        if os.path.isfile(file_path) and file.lower().endswith(image_extensions):

            try:
                # Try getting EXIF date
                taken_date = get_photo_taken_date(file_path)

                if taken_date:
                    year = taken_date.strftime("%Y")
                else:
                    # Fallback to file modified time
                    timestamp = os.path.getmtime(file_path)
                    year = datetime.fromtimestamp(timestamp).strftime("%Y")

                # Create year folder
                year_folder = os.path.join(destination_folder, year)
                os.makedirs(year_folder, exist_ok=True)

                # Handle duplicate file names
                destination_path = os.path.join(year_folder, file)
                counter = 1
                while os.path.exists(destination_path):
                    name, ext = os.path.splitext(file)
                    destination_path = os.path.join(year_folder, f"{name}_{counter}{ext}")
                    counter += 1

                shutil.move(file_path, destination_path)
                print(f"Moved: {file} → {year}")

            except Exception as e:
                print(f"Error processing {file}: {e}")


if __name__ == "__main__":
    source = "D:/Cat/old photos"
    destination = "D:/Cat/Photo group"

    organize_photos_by_year(source, destination)
    print("Done organizing photos!")
