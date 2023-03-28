# define asset path
import datetime
import os
import re
import subprocess
import sys

import humanize

# get post name from the first argument
post_name = sys.argv[1]

post_parent_path = '{}/source/_posts/'.format(os.getcwd())
post_path = '{}{}.md'.format(post_parent_path, post_name)

origin_asset_path = '{}assets/'.format(post_parent_path)
target_image_path = '{}/source/img/'.format(os.getcwd())


# get all assets in the origin asset folder
origin_assets = os.listdir(origin_asset_path)

# compress the png in the origin asset folder
for asset in origin_assets:
    print('compressing {}'.format(asset))
    # get size of the png
    origin_size = os.path.getsize('{}/{}'.format(origin_asset_path, asset))
    os.system('/opt/homebrew/bin/pngquant --force --ext .png --speed 1 --quality 65-80 {}/{}'.format(origin_asset_path, asset))
    # get the size of the png after compressing
    compressed_size = os.path.getsize('{}/{}'.format(origin_asset_path, asset))
    # print the size of the png before and after compressing with human readable
    print('compress {} origin size: {} compressed size: {}'.format(asset, humanize.naturalsize(origin_size), humanize.naturalsize(compressed_size)))
    # move the compressed png to the target image folder
    print('moving {} to {}'.format(asset, target_image_path))
    os.system('mv {}/{} {}'.format(origin_asset_path, asset, target_image_path))

# delete asset path
print('deleting {}'.format(origin_asset_path))
subprocess.call(['rm', '-r', origin_asset_path])

# read the post file and find all assets define like ![](assets/image.png) and replace them with ![](/img/image.png)
print('replacing assets path in {}'.format(post_path))
with open(post_path, 'r') as file:
    filedata = file.read()
    assets = re.findall(r'!\[\]\(assets/(.*?)\)', filedata)

    # replace the assets path in the post file
    for i, asset in enumerate(assets):
        # replace the asset path in the markdown file
        print('replacing ![](assets/{}) with ![](/img/{})'.format(asset, asset))
        filedata = filedata.replace('![](assets/{})'.format(asset), '![](/img/{})'.format(asset))

    print('updated date replaced with {}'.format(datetime.datetime.now().strftime('%Y-%m-%d')))
    # find 'updated: year-month-day' and replace it with today date
    filedata = re.sub(r'updated: \d{4}-\d{2}-\d{2}', 'updated: {}'.format(datetime.datetime.now().strftime('%Y-%m-%d')), filedata)

    # write filedata to the target markdown file
    with open(post_path, 'w') as file:
        file.write(filedata)

