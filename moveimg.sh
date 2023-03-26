#!/usr/bin/env bash

source_img_dir="source/_posts/assets"
target_img_dir="source/img"

echo "move Atom generate images $source_img_dir/ to the $target_img_dir folder"
mv $source_img_dir/* $target_img_dir

echo "delete the $source_img_dir folder"
rm -rf $source_img_dir
