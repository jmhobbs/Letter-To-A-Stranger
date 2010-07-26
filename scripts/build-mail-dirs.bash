#! /usr/bin/env bash

# This script will build the very deep tree of directories for LTAS mail storage.

if [ "1" != "$#" ]; then
	echo "Usage: $0 [path]"
	exit
fi

if [ ! -d "$1" ]; then
	echo "ERROR: $1 is not a valid path"
	exit
fi

if [ "/" != "$(echo $1 | sed 's/^.*\(.$\)/\1/' )" ]; then
	CREATE_PATH="$1/"
else
	CREATE_PATH="$1"
fi

echo "Building mail directories based at $CREATE_PATH. Please wait."

mkdir -p ${CREATE_PATH}mail/{full,clean}/{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9}/{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z,0,1,2,3,4,5,6,7,8,9}

if [ "" != "$(which tree)" ]; then
	echo "Loading tree, press enter to coninue"
	read nop
	tree -dfi $CREATE_PATH | less
else
	echo "Your system doesn't have 'tree' installed."
	echo "Check your install manually by browsing '$CREATE_PATH'"
	echo "Have fun!"
fi
