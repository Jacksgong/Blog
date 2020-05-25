#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.
set -e

echo "$(tput setaf 3)---------Public-Release v3.0--------- $(tput sgr 0)"

echo "$(tput setaf 3)>>>>>>start generate blog$(tput sgr 0)"
hexo g
echo "$(tput setaf 3)<<<<<<finish generate blog$(tput sgr 0)"

echo "$(tput setaf 3)>>>>>>start push source code$(tput sgr 0)"
bash push-double-end.sh
echo "$(tput setaf 3)<<<<<<finish push source code$(tput sgr 0)"

echo "$(tput setaf 3)>>>>>>start push blog$(tput sgr 0)"
cd public
rm -rf .git
git init
git remote add origin git@git.dreamtobe.cn:Jacksgong/blog-deploy.git

# Commit:
commit_date="$(date)"
git add --all
commit_msg="normal commit: $commit_date"
git commit -m "$commit_msg"

# Push:
git push --force origin master
echo "$(tput setaf 3)>>>>>>fninsh push blog$(tput sgr 0)"

# add marker
echo "$(tput setaf 3)>>>>>>start add deploy marker$(tput sgr 0)"
git clone git@git.dreamtobe.cn:Jacksgong/blog-deploy-auto-marker.git deploy-marker
cd deploy-marker
bash add-deploy.sh
cd ..
rm -rf deploy-marker
echo "$(tput setaf 3)<<<<<<finish add deploy marker$(tput sgr 0)"
