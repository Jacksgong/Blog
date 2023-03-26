# title: 流利说客户端持续交付工程实践
# date: 2018-08-15 22:07:03
# updated: 2018-12-15
# permalink: openclash_maintain
# categories:
# - 持续交付
# tags:
# - Android
# - 持续交付
# - 英语流利说
# - GitLabCI
# 
# ---
# 
# {% note info %} 这块持续交付体系是一套比较系统化的、可靠的解决方案，也是我们这几年摸索沉淀的结果，希望大家都能够从中有所收益。{% endnote %}
# 
# <!-- more -->

# get title from the first argument
import sys
title = sys.argv[1]

# remove .md suffix from title if it exists
if title.endswith('.md'):
    title = title[:-3]

# generate date like 2018-08-15 22:07:03
import datetime
date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# generate updated like 2018-12-15
updated = datetime.datetime.now().strftime('%Y-%m-%d')

print('title: {}'.format(title))
print('date: {}'.format(date))
print('updated: {}'.format(updated))
print('permalink: ')
print('categories:')
print('- fun')
print('tags:')
print('- python')
print('')
print('---')
print('')
print('{% note info %} empty {% endnote %}')
print('')
print('<!-- more -->')