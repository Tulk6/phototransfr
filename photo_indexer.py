import os, shutil

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
        manifest[f'{current_photo_index}.jpg'] = folder+'/'+photo
        shutil.copy2(src_file, dst_file)
        current_photo_index += 1

print(sum_photos)

with open('photo_manifest.txt', 'w') as f:
    f.write(str(manifest))