#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.
set -e

echo "$(tput setaf 3)---------Public-Release v4.0--------- $(tput sgr 0)"

echo "$(tput setaf 3)>>>>>>start generate blog$(tput sgr 0)"
hexo g
echo "$(tput setaf 3)<<<<<<finish generate blog$(tput sgr 0)"

#echo "$(tput setaf 3)>>>>>>start push source code$(tput sgr 0)"
#bash push-double-end.sh
#echo "$(tput setaf 3)<<<<<<finish push source code$(tput sgr 0)"

echo "$(tput setaf 3)>>>>>>start push blog$(tput sgr 0)"
cd public
rm -rf .git
git init
git remote add origin ssh://git@gitea.partyland.cc:2222/jacks/blog-deploy.git

# Commit:
commit_date="$(date)"
git add --all
commit_msg="normal commit: $commit_date"
git commit -m "$commit_msg"

# Push:
git checkout -b master
git push --force origin master
echo "$(tput setaf 3)>>>>>>fninsh push blog$(tput sgr 0)"

# add marker
echo "$(tput setaf 3)>>>>>>start add deploy marker$(tput sgr 0)"
git clone ssh://git@gitea.partyland.cc:2222/jacks/blog-deploy-auto-marker.git deploy-marker
cd deploy-marker

bash add-deploy.sh
cd ..
rm -rf deploy-marker
echo "$(tput setaf 3)<<<<<<finish add deploy marker$(tput sgr 0)"
