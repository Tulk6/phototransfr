import os, shutil, datetime, json
from PIL import Image, ExifTags

def get_number_of_files_in_folder(path):
    return len(os.listdir(path))

dcim_dir = ""
out_folder = ""

if dcim_dir == "" or out_folder == "":
    raise ValueError("Paths must be provided for dcim_dir (source of photos) and out_dir (where sorted photos are placed)")

manifest = {}

all_photos = []

sum_photos = 0
for folder in os.listdir(dcim_dir):
    sum_photos += len(os.listdir(dcim_dir+folder))

for folder in os.listdir(dcim_dir):
    for photo in os.listdir(dcim_dir+folder):
        src_file = dcim_dir+folder+'/'+photo
        print(src_file)
        img = Image.open(src_file)
        img_exif = img.getexif()
        try:
            datetime_str = img_exif[ExifTags.Base.DateTime]
        except KeyError:
            datetime_srt = '1970:01:01 00:00:00'
        datetime_obj = datetime.datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
        datetime_formatted = datetime.datetime.strftime(datetime_obj, '%A, %d %b, %Y at %X')
        epoch = datetime_obj.timestamp()
        try:
            caption = img_exif[ExifTags.Base.ImageDescription]
        except KeyError:
            caption = ''
        img.close()

        all_photos.append({'src': src_file, 'caption': caption, 'datetime': datetime_formatted, 'epoch': epoch})

all_photos = sorted(all_photos, key = lambda x: x['epoch'])

current_photo_index = 0
for current_photo_index, photo in enumerate(all_photos):
    dst_file = out_folder+f'{current_photo_index}.jpg'
    src_file = photo['src']

    manifest[str(current_photo_index)] = {'src': photo['src'], 'datetime': photo['datetime'], 'caption': photo['caption']}
    shutil.copy2(src_file, dst_file)
    current_photo_index += 1
    print(current_photo_index)

print(sum_photos)

with open(out_dir+'photo_manifest.txt', 'w') as f:
    f.write(json.dumps(manifest))