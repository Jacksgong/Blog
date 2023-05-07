import hashlib
import os
import re
import sys
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

# 处理![[post#subtitle]]这样的文章内链引用
def replace_obsidian(filedata, path_of_obsidian_valt, parent_ref_list=[]):
    # find 'post' and 'subtitle' from read content like '![[post#subtitle]]'
    obsidian_content = re.findall(r'!\[\[(.*?)\]\]', filedata)
    # if not match the pattern, then skip
    if len(obsidian_content) == 0:
        return filedata

    replaced_filedata = filedata
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
        parent_ref_list.append(obsidian)

        # find file with post.md by traversing path_of_obsidian_valt directory
        post_file_path = ''
        for root, dirs, files in os.walk(path_of_obsidian_valt):
            for file in files:
                if file == post + '.md':
                    post_file_path = os.path.join(root, file)
                    break

        # if the post not exist in the path_of_obsidian_valt, then skip
        if not os.path.exists(post_file_path):
            print('post {} not exist!!!'.format(post))
            continue

        # read the post file
        with open(post_file_path, 'r') as post_file:
            post_filedata = post_file.read()
            # 找出subtitle所在行，在subtitle之前有几个#
            subtitle_level = len(re.findall(r'^#+ {}'.format(subtitle), post_filedata, re.MULTILINE)[0].split(' ')[0])

            subtitle_content = ''
            begine_assemble = False
            code_block = False
            skip_line_with_loop = False # new variable to track if current line contains a nested loop
            for line in post_filedata.split('\n'):
                if line.startswith('#'):
                    # if the content is start with '#' and end with subtitle, then begine assemble the content
                    if line.startswith('#') and line.endswith(subtitle):
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
                        break
                    # if this line contains a nested loop, skip it
                    if skip_line_with_loop:
                        skip_line_with_loop = False
                        continue

                    # 避免循环依赖，如果当前行包含父级引用，则跳过
                    for parent_ref in parent_ref_list:
                        if parent_ref in line:
                            print('parent_ref({}) in the line({}), so ignore line'.format(parent_ref, line))
                            continue

                    subtitle_content += line + '\n'

            # if not match the subtitle, then skip
            if len(subtitle_content) == 0:
                continue

            # 处理当前层级的引用
            replaced_subtitle_content = replace_obsidian(subtitle_content, path_of_obsidian_valt, parent_ref_list)

            # 将target_markdown_file_path中的![[post#subtitle]]替换为subtitle_content
            replaced_filedata = replaced_filedata.replace('![[{}#{}]]'.format(post, subtitle), replaced_subtitle_content)

    return replaced_filedata


# read each line from target_markdown_file_path and replace all obsidian content links in target_markdown_file_path like ![[post#subtitle]] to target real content in the post file and rewrite the target_markdown_file_path
print('read each line from $target_markdown_file_path and replace all obsidian content links in target_markdown_file_path like ![[post#subtitle]] to target real content in the post file and rewrite the target_markdown_file_path')
with open(target_markdown_file_path, 'r') as file:
    # read each line from file
    filedata = file.read()
    
    # replace all obsidian content links in target_markdown_file_path like ![[post#subtitle]] to target real content in the post file and rewrite the target_markdown_file_path
    filedata = replace_obsidian(filedata, path_of_obsidian_valt)

    # write filedata to the target markdown file
    with open(target_markdown_file_path, 'w') as file:
        file.write(filedata)

# 处理图片
# read the file and found all assets define like ![[image.png]] in the target markdown file
with open(target_markdown_file_path, 'r') as file:
    filedata = file.read()
    assets = re.findall(r'!\[\[(.*?)\]\]', filedata)
    target_assets = []
    using_assets = []

    # copy the assets to the target asset folder and make their name as markdown file name + incremental number
    print('copy the assets to the target asset folder and make their name as markdown file name + incremental number')
    for i, asset in enumerate(assets):
        # get the suffix from the asset path
        suffix = asset.split('.')[-1]

        # genereate short md5 hash for the asset
        md5_hash = hashlib.md5(asset.encode('utf-8')).hexdigest()[:8]

        # generate the target asset file name
        target_asset_file_name = '{}_{}_{}.{}'.format(target_markdown_file_name, md5_hash,i, suffix)

        # record in using assets
        using_assets.append(target_asset_file_name)

        # if the target asset file exist, then skip
        if os.path.exists('{}/{}'.format(target_asset_folder, target_asset_file_name)):
            print('target asset file({}) exist, skip'.format(target_asset_file_name))
            continue

        # copy the asset to the target asset folder
        print('copying {} to {}'.format(asset, '{}/{}'.format(target_asset_folder, target_asset_file_name)))
        with open('{}/{}'.format(obsidian_assset_folder, asset), 'rb') as asset_file:
            with open('{}/{}'.format(target_asset_folder, target_asset_file_name), 'wb') as target_asset_file:
                target_asset_file.write(asset_file.read())

        # assign the new asset path to the target_assets
        target_assets.append(target_asset_file_name)

    # if asset is not in using_assets and prefix name is target_markdown_file_name in the target asset folder, then delete it
    print('if asset is not in using_assets(size:{}) and prefix name is {} in the {}, then delete it'.format(len(using_assets), target_markdown_file_name, target_asset_folder))
    deleted_assets = []
    for asset in os.listdir(target_asset_folder):
        if asset.startswith(target_markdown_file_name) and asset not in using_assets:
            print('deleting {}'.format(asset))
            os.remove('{}/{}'.format(target_asset_folder, asset))
            deleted_assets.append(asset)
    print('deleted assets size: {}'.format(len(deleted_assets))) 

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
        print('replacing {} to {}'.format(asset, using_assets[i]))
        filedata = filedata.replace('![[{}]]'.format(asset), '![](/img/{})'.format(using_assets[i]))

    # write filedata to the target markdown file
    with open(target_markdown_file_path, 'w') as file:
        file.write(filedata)

# print success message
print('success')