#!/usr/bin/env bash
set -ex
PROJECT_NAME=$1

TEMPLATE_PROJECT='collection_template'

git reset "$(git rev-list --max-parents=0 --abbrev-commit HEAD)"
find . -type f -exec sed -i -e "s/$TEMPLATE_PROJECT/$PROJECT_NAME/g" {} \;
find . -type f -exec sed -i -e "s/{{ YEAR }}/$(date +'%Y')/g" {} \;
mv __example_app__ "$PACKAGE_NAME"
rm -f "$0"

git add .
git commit -am "Initial"
