#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.

rm -rf public/.git
cp -r ../.blog-deploy-git public/.git
cd public
echo "$(tput setaf 3)---------Public-Release v1.0--------- $(tput sgr 0)"

# Commit:
commit_date="$(date)"
git add --all
commit_msg="normal commit: $commit_date"
git commit -m "$commit_msg"

# Push:
git fetch origin
git rebase -Xtheirs origin/master
git push

echo "$(tput setaf 3)Has successfully cimmit: $commit_msg$(tput sgr 0)"
cd ..
rm -rf ../.blog-deploy-git
cp public/.git ../.blog-deploy-git
