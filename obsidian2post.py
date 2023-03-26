
import os
import re
import sys
import humanize

path_of_obsidian_valt = sys.argv[1]
obsidian_assset_folder= path_of_obsidian_valt + '/assets'
ob_markdown_file_path = sys.argv[2]

# if the third argument is not empty, then use the third argument as the target markdown file name
if len(sys.argv) > 3:
    target_markdown_file_name = sys.argv[3]
    target_markdown_file_path = '{}/source/_posts/{}.md'.format(os.getcwd(), sys.argv[3])
else:
    target_markdown_file_name = ob_markdown_file_path.split('/')[-1].split('.')[0]

# target markdown file path equal to the current folder + source/_posts + target_markdown_file_name + .md
target_markdown_file_path = '{}/source/_posts/{}.md'.format(os.getcwd(), target_markdown_file_name)

# target asset folder equal to the current folder + source/img
target_asset_folder = os.getcwd() + '/source/img'

# output all arguments
print('path_of_obsidian_valt: {}'.format(path_of_obsidian_valt))
print('obsidian_assset_folder: {}'.format(obsidian_assset_folder))
print('ob_markdown_file_path: {}'.format(ob_markdown_file_path))
print('target_markdown_file_name: {}'.format(target_markdown_file_name))

print('target_markdown_file_path: {}'.format(target_markdown_file_path))
print('target_asset_folder: {}'.format(target_asset_folder))

# ouput the empty line
print('')

# delete target markdown file if it exists
if os.path.exists(target_markdown_file_path):
    print('deleting {}'.format(target_markdown_file_path))
    os.remove(target_markdown_file_path)

# copy the markdown file to the target path
print('copy the markdown file to the target path')
with open(ob_markdown_file_path, 'r') as file:
    filedata = file.read()
    with open(target_markdown_file_path, 'w') as target_file:
        target_file.write(filedata)

# delete prefix name is target_markdown_file_name in the target asset folder
print('delete prefix name is target_markdown_file_name in the target asset folder')
for file in os.listdir(target_asset_folder):
    if file.startswith(target_markdown_file_name + '_'):
        print('deleting {}'.format(file))
        os.remove('{}/{}'.format(target_asset_folder, file))

# read the file and found all assets define like ![[image.png]] in the target markdown file
with open(target_markdown_file_path, 'r') as file:
    filedata = file.read()
    assets = re.findall(r'!\[\[(.*?)\]\]', filedata)
    target_assets = []

    # copy the assets to the target asset folder and make their name as markdown file name + incremental number
    print('copy the assets to the target asset folder and make their name as markdown file name + incremental number')
    for i, asset in enumerate(assets):
        # get the suffix from the asset path
        suffix = asset.split('.')[-1]

        target_asset_file_name = '{}_{}.{}'.format(target_markdown_file_name, i, suffix)
        print('copying {} to {}'.format(asset, '{}/{}'.format(target_asset_folder, target_asset_file_name)))

        with open('{}/{}'.format(obsidian_assset_folder, asset), 'rb') as asset_file:
            with open('{}/{}'.format(target_asset_folder, target_asset_file_name), 'wb') as target_asset_file:
                target_asset_file.write(asset_file.read())
        # assign the new asset path to the target_assets
        target_assets.append(target_asset_file_name)
       
    # compress the png in the target asset folder
    for asset in target_assets:
        if asset.split('.')[-1] == 'png':
            print('compressing {}'.format(asset))
            # get size of the png
            origin_size = os.path.getsize('{}/{}'.format(target_asset_folder, asset))
            os.system('pngquant --force --ext .png --speed 1 --quality 60-80 {}/{}'.format(target_asset_folder, asset))
            # get the size of the png after compressing
            compressed_size = os.path.getsize('{}/{}'.format(target_asset_folder, asset))
            # print the size of the png before and after compressing with human readable
        print('origin size: {} compressed size: {}'.format(humanize.naturalsize(origin_size), humanize.naturalsize(compressed_size)))

    # replace the assets path in the markdown file
    for i, asset in enumerate(assets):
        # replace the asset path in the markdown file
        print('replacing {} to {}'.format(asset, target_assets[i]))
        filedata = filedata.replace('![[{}]]'.format(asset), '![](/img/{})'.format(target_assets[i]))
        # write filedata to the target markdown file
        with open(target_markdown_file_path, 'w') as file:
            file.write(filedata)