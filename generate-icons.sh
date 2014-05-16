#!/bin/bash
# Usage: generate-icons.sh bigicon.png destpath/

convert $1 -resize 57x57   $2/Icon.png
convert $1 -resize 114x114 $2/Icon@2x.png
convert $1 -resize 120x120 $2/Icon-60@2x.png
convert $1 -resize 72x72   $2/Icon-72.png
convert $1 -resize 144x44  $2/Icon-72@2x.png
convert $1 -resize 76x76   $2/Icon-76.png
convert $1 -resize 152x152 $2/Icon-76@2x.png
convert $1 -resize 29x29   $2/Icon-Small.png
convert $1 -resize 58x58   $2/Icon-Small@2x.png
convert $1 -resize 40x40   $2/Icon-Small-40.png
convert $1 -resize 80x80   $2/Icon-Small-40@2x.png
convert $1 -resize 50x50   $2/Icon-Small-50.png
convert $1 -resize 100x100 $2/Icon-Small-50@2x.png