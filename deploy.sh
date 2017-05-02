#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.

echo "$(tput setaf 3)---------Public-Release v2.0--------- $(tput sgr 0)"

bash push-double-end.sh
cd public
rm -rf .git
git init
git remote add origin git@git.jacksgong.com:Jacksgong/blog-deploy.git

# Commit:
commit_date="$(date)"
git add --all
commit_msg="normal commit: $commit_date"
git commit -m "$commit_msg"

# Push:
git push --force origin master
echo "$(tput setaf 3)Has successfully cimmit: $commit_msg$(tput sgr 0)"
