#!/bin/bash
if [ -f /.dockerenv ]; then
   echo "You can not start the development environment inside a docker container"
else
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
	pushd "$DIR" >/dev/null
	VERSION=$(grep --max-count=1 'version' app/main.py | awk -F '"' '{ print $2 }' | awk -F '"' '{ print $1 }')
	DOCKER_BUILDKIT=1 docker build -f docker/Dockerfile -t internetofus/profile-diversity-manager:$VERSION .
	if [ $? -eq 0 ]; then
		docker tag internetofus/profile-diversity-manager:$VERSION internetofus/profile-diversity-manager:latest
		DOCKER_BUILDKIT=1 docker build -f docker/dev/Dockerfile -t internetofus/profile-diversity-manager:dev .
		docker run --rm --name profile_diversity_manager_dev -v "${PWD}":/app -p 9000:9000 -it internetofus/profile-diversity-manager:dev /bin/bash
	fi
	popd >/dev/null
fi