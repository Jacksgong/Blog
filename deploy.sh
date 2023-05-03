#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.
set -e

echo "==========---------Public-Release v4.0--------- =========="
hexo -v
node -v
npm -v

echo "==========>>>>>>prepare private key=========="
cp /opt/blog/.env .env
echo "==========>>>>>>start generate blog=========="
python3 run_with_private_key.py g
ls
echo "==========<<<<<<finish generate blog=========="

#echo "==========>>>>>>start push source code=========="
#bash push-double-end.sh
#echo "==========<<<<<<finish push source code=========="

echo "==========>>>>>>start push blog=========="
cd public
ls
rm -rf .git
git init
git remote add origin ssh://git@gitea.partyland.cc:2222/jacks/blog-deploy.git

# Commit:
commit_date="$(date)"
git add --all
commit_msg="normal commit: $commit_date"
git commit -m "$commit_msg"

# Push:
git checkout -B master
git push --force origin master
echo "==========>>>>>>fninsh push blog=========="

# add marker
echo "==========>>>>>>start add deploy marker=========="
git clone ssh://git@gitea.partyland.cc:2222/jacks/blog-deploy-auto-marker.git deploy-marker
cd deploy-marker

bash add-deploy.sh
cd ..
rm -rf deploy-marker
echo "==========<<<<<<finish add deploy marker=========="
