#!/bin/bash
if ! docker stats --no-stream >/dev/null 2>&1; then
    echo "Docker does not seem to be running, run it first and retry"
    exit 1
else
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
	pushd "$DIR" > /dev/null
	VERSION=$(grep --max-count=1 'version' app/main.py | awk -F '"' '{ print $2 }' | awk -F '"' '{ print $1 }')
	DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile -t internetofus/profile-diversity-manager:$VERSION .
	popd > /dev/null	
fi
