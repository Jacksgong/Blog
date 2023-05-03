import os
import shutil

# 读取第一个变量作为要执行的命令
command = os.sys.argv[1]

# 获取.env和_config.fluid.yml文件路径
env_file_path = os.path.join(os.getcwd(), '.env')
config_file_path = os.path.join(os.getcwd(), '_config.fluid.yml')

# 创建临时文件
temp_config_file_path = 'temp_config.fluid.yml'

# 打开.env文件
with open(env_file_path, 'r', encoding='utf-8') as f1, \
     open(config_file_path, 'r', encoding='utf-8') as f2, \
     open(temp_config_file_path, 'w', encoding='utf-8') as f3:

    # 读取.env文件内容
    env_content = f1.read()

    # 读取_config.fluid.yml文件内容
    config_content = f2.read()

    # 按行分割.env内容
    env_lines = env_content.split('\n')

    # 遍历.env每一行
    for env_line in env_lines:
        if env_line:
            # 查找环境变量名称和值
            env_var, env_val = env_line.split('=', maxsplit=1)

            # 构建替换字符串
            replace_str = '$' + env_var
            print(replace_str, env_val)

            # 替换字符串
            config_content = config_content.replace(replace_str, env_val)

    # 将替换后的内容写入临时文件
    f3.write(config_content)


# 备份原_config.fluid.yml文件
backup_config_file_path = os.path.join(os.getcwd(), '_config.fluid.yml.bak')
shutil.move(config_file_path, backup_config_file_path)

# 将替换后的文件重命名为_config.fluid.yml
shutil.move(temp_config_file_path, config_file_path)

try:
    # 执行hexo g -d命令
    if command == 'g':
        os.system('hexo g')
    elif command == 's':
        os.system('hexo s')
finally:
    # 删除临时文件
    os.remove(config_file_path)

    # 恢复原_config.fluid.yml文件
    shutil.move(backup_config_file_path, config_file_path)