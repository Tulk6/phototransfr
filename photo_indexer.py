import os, shutil, datetime, json
from PIL import Image, ExifTags

def get_number_of_files_in_folder(path):
    return len(os.listdir(path))

dcim_dir = "E:/best_photos/"
out_folder = "static/photos/"

manifest = {}

sum_photos = 0
for folder in os.listdir(dcim_dir):
    sum_photos += len(os.listdir(dcim_dir+folder))

current_photo_index = 0
for folder in os.listdir(dcim_dir):
    for photo in os.listdir(dcim_dir+folder):
        dst_file = out_folder+f'{current_photo_index}.jpg'
        src_file = dcim_dir+folder+'/'+photo

        img = Image.open(src_file)
        img_exif = img.getexif()
        datetime_str = img_exif[ExifTags.Base.DateTime]
        datetime_obj = datetime.datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
        datetime_formatted = datetime.datetime.strftime(datetime_obj, '%A, %d %b, %Y at %X')
        caption = img_exif[ExifTags.Base.ImageDescription]
        img.close()

        manifest[str(current_photo_index)] = {'src': folder+'/'+photo, 'datetime': datetime_formatted, 'caption': caption}
        shutil.copy2(src_file, dst_file)
        current_photo_index += 1

print(sum_photos)

with open('photo_manifest.txt', 'w') as f:
    f.write(json.dumps(manifest))