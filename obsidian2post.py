import os
import re
import sys
import uuid
import humanize

blog_root_path = sys.argv[1]
path_of_obsidian_valt = sys.argv[2]
obsidian_assset_folder= path_of_obsidian_valt + '/assets'
ob_markdown_file_path = sys.argv[3]

# if the third argument is not empty, then use the third argument as the target markdown file name
if len(sys.argv) > 4:
    target_markdown_file_name = sys.argv[4]
    target_markdown_file_path = '{}/source/_posts/{}.md'.format(blog_root_path, sys.argv[4])
else:
    target_markdown_file_name = ob_markdown_file_path.split('/')[-1].split('.')[0]

# target markdown file path equal to the current folder + source/_posts + target_markdown_file_name + .md
target_markdown_file_path = '{}/source/_posts/{}.md'.format(blog_root_path, target_markdown_file_name)

# target asset folder equal to the current folder + source/img
target_asset_folder = blog_root_path + '/source/img'

# output all arguments
print('blog_root_path: {}'.format(blog_root_path))
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


# read each line from target_markdown_file_path and replace all obsidian content links in target_markdown_file_path like ![[post#subtitle]] to target real content in the post file and rewrite the target_markdown_file_path
print('read each line from $target_markdown_file_path and replace all obsidian content links in target_markdown_file_path like ![[post#subtitle]] to target real content in the post file and rewrite the target_markdown_file_path')
with open(target_markdown_file_path, 'r') as file:
    # read each line from file
    filedata = file.read()
    # find 'post' and 'subtitle' from read content like '![[post#subtitle]]'
    obsidian_content = re.findall(r'!\[\[(.*?)\]\]', filedata)
    # if not match the pattern, then skip
    if len(obsidian_content) == 0:
        print('not match the pattern, skip')
        exit(0)

    # write filedata to the target markdown file
    with open(target_markdown_file_path, 'w') as file:
        file.write(filedata)

    # replace all obsidian content links in target_markdown_file_path like ![[post#subtitle]] to target real content in the post file and rewrite the target_markdown_file_path
    for obsidian in obsidian_content:
        # split the obsidian by '#'
        obsidian_split = obsidian.split('#')
        # if the obsidian not contain '#', then skip
        if len(obsidian_split) == 1:
            continue

        # get the post and subtitle from the obsidian
        post = obsidian_split[0]
        subtitle = obsidian_split[1]

        print('post: {}, subtitle: {}'.format(post, subtitle))

        # find file with post.md by traversing path_of_obsidian_valt directory
        post_file_path = ''
        for root, dirs, files in os.walk(path_of_obsidian_valt):
            for file in files:
                if file == post + '.md':
                    post_file_path = os.path.join(root, file)
                    break

        print('post_file_path: {}'.format(post_file_path))
        # if the post not exist in the path_of_obsidian_valt, then skip
        if not os.path.exists(post_file_path):
            print('not exist {} in {}'.format(post_file_path, path_of_obsidian_valt))
            continue

        # if the post not exist in the path_of_obsidian_valt, then skip
        if not os.path.exists(post_file_path):
            print('not exist {} in {}'.format(post_file_path, path_of_obsidian_valt))
            continue

        # read the post file
        with open(post_file_path, 'r') as post_file:
            post_filedata = post_file.read()
            # 找出subtitle所在行，在subtitle之前有几个#
            subtitle_level = len(re.findall(r'^#+ {}'.format(subtitle), post_filedata, re.MULTILINE)[0].split(' ')[0])
            print('subtitle_level: {}'.format(subtitle_level))

            subtitle_content = ''
            begine_assemble = False
            code_block = False
            for line in post_filedata.split('\n'):
                if line.startswith('#'):
                    # if the content is start with '#' and end with subtitle, then begine assemble the content
                    if line.startswith('#') and line.endswith(subtitle):
                        print('begine assemble the content with {}'.format(line))
                        begine_assemble = True
                        continue

                # if begine assemble the content, then assemble the content
                if begine_assemble:
                    # if the content is start with '```', then set code_block to True
                    if not code_block and line.startswith('```'):
                        code_block = True
                    # if the content is end with '```' and code_block is True, then set code_block to False
                    if code_block and line.endswith('```'):
                        code_block = False

                    # if the content is start with '#' and subtitle_level is same or higher than subtitle_level, then end assemble the content
                    if line.startswith('#') and len(line.split(' ')[0]) <= subtitle_level and not code_block:
                        print('end assemble the content with {}'.format(line))
                        break
                    subtitle_content += line + '\n'

            print('subtitle_content: {}'.format(subtitle_content))

            # if not match the subtitle, then skip
            if len(subtitle_content) == 0:
                print('not match the subtitle, skip')
                continue

            # 将subtitle_content列表中的所有的内容拼接起来
            subtitle_content = ''.join(subtitle_content)

            # 将target_markdown_file_path中的![[post#subtitle]]替换为subtitle_content
            filedata = filedata.replace('![[{}#{}]]'.format(post, subtitle), subtitle_content)

        # write filedata to the target markdown file
        with open(target_markdown_file_path, 'w') as file:
            file.write(filedata)

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

        # generate uuid for the asset file name for avoid web server cache
        target_asset_file_name = '{}_{}_{}.{}'.format(target_markdown_file_name, i, uuid.uuid4(), suffix)
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
            os.system('/opt/homebrew/bin/pngquant --force --ext .png --speed 1 --quality 60-80 {}/{}'.format(target_asset_folder, asset))
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

# print success message
print('success')