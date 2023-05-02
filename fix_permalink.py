import os

# 获取当前目录
current_dir = os.getcwd() + '/source/_posts'
# 遍历当前目录下的所有文件和文件夹
for root, dirs, files in os.walk(current_dir):
    for file in files:
        # 判断文件是否为.md文件
        if file.endswith('.md'):
            # 获取文件路径
            file_path = os.path.join(root, file)
            # 读取文件内容
            with open(file_path, 'r+', encoding='utf-8') as f:
                content = f.read()
                # 查找"permalink: <content>"的位置
                start = content.find('permalink: ')
                if start != -1:
                    end = content.find('\n', start)
                    permalink = content[start:end].split(':')[1].strip()
                    # 判断permalink是否以'/'结尾
                    if not permalink.endswith('/'):
                        # 如果不是，替换为以'/'结尾的permalink
                        #f.seek(start)
                        #f.write('permalink: {}/{}'.format(permalink, '\n'))

                        # 将'permalink: <content>'替换为'permalink: <content>/'
                        content = content.replace('permalink: {}'.format(permalink), 'permalink: {}/'.format(permalink))
                        # 写入文件
                        f.seek(0)
                        f.write(content)
                        # 打印修改信息
                        print('修改成功：{}'.format(file_path))
                        print('修改前：{}'.format(content[start:end]))
                        print('修改后：{}'.format('permalink: {}/{}'.format(permalink, '\n')))
