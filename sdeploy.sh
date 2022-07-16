#!/bin/bash
# @author Jacksgong
#
# @version 1.0.0
#
# For deplay public folder.

echo "$(tput setaf 3)---------Server Deploy v1.0--------- $(tput sgr 0)"
rm -rf public
git clone git@gitea.partyland.cc:2222/jacks/blog-deploy.git public

echo "$(tput setaf 3)Has successfully deploy to server$(tput sgr 0)"
