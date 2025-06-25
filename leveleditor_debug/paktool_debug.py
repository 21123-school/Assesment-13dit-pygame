import os
import zipfile
    
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

name = 'data'#input('name folder for compression: ')
try:
    os.remove(f"{name}.pak")
    print('old file removed making new file..')
except:
    print('not found making new file..')
with zipfile.ZipFile(f'..\{name}.pak', 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipdir(f'{name}/', zipf)
    print('new file created..')
#input('press enter to close..')
