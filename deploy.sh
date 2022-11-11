#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.
set -e

if [[ $- == *i* ]]; then
  fgRed=$(tput setaf 1)     ; fgGreen=$(tput setaf 2)  ; fgBlue=$(tput setaf 4)
  fgMagenta=$(tput setaf 5) ; fgYellow=$(tput setaf 3) ; fgCyan=$(tput setaf 6)
  fgWhite=$(tput setaf 7)   ; fgBlack=$(tput setaf 0)
  bgRed=$(tput setab 1)     ; bgGreen=$(tput setab 2)  ; bgBlue=$(tput setab 4)
  bgMagenta=$(tput setab 5) ; bgYellow=$(tput setab 3) ; bgCyan=$(tput setab 6)
  bgWhite=$(tput setab 7)   ; bgBlack=$(tput setab 0)
fi

echo "$(tput setaf 3)---------Public-Release v4.0--------- $(tput sgr 0)"
hexo -v
node -v
npm -v

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
