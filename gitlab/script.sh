#!/bin/bash 

cd /home/gitlab/workspace/gitlab/

cloneurl=$1

efsfsid="fs-07883c47"

wpversion="5.8.3"

phpversion="7.4"

#Remove everything before '/' in the clone url and remove '.git' part from the URL to get the project folder name
livedomain=$cloneurl
livedomain="sed 's@.*/@@' $livedomain"
livedomain=$(echo $livedomain | sed 's@.*/@@' | sed 's/\.[^.]*$//g')
livedomain="$livedomain"
echo "Live Domain: $livedomain"

#Replace every occurance of '.' from '-' from the project folder to determine appname
liveappname=$(echo $livedomain | sed 's/\./-/g')

echo "Live App Name: $liveappname"

e=$(echo $livedomain | cut -d. -f2-)
localdomain=local.$e
echo "Local Domain: $localdomain"

d=$(echo $livedomain | cut -d. -f2- | rev | cut -d. -f2- | rev)
previewdomain=$d.emarketingeye.net
echo "Preview Domain: $previewdomain"
previewappname=$(echo $previewdomain | sed 's/\./-/g')
echo "Preview App Name: $previewappname"

rm -rf wordpress-sample.git
echo "Downloading wordpress-sample.git ........."
git clone --bare git@gitlab.com:de155/wordpress-sample.git wordpress-sample.git
cd wordpress-sample.git && git push --mirror $cloneurl && cd ..
git clone $cloneurl -b develop && cd $livedomain

sed -i "s@LIVE_EFS_FS: EFS_ID@LIVE_EFS_FS: $efsfsid@g" .gitlab-ci.yml
sed -i "s@LIVE_DOMAIN: www.example.com@LIVE_DOMAIN: $livedomain@g" .gitlab-ci.yml
sed -i "s@LIVE_APP_NAME: www-example-com@LIVE_APP_NAME: $liveappname@g" .gitlab-ci.yml
sed -i "s@PREVIEW_DOMAIN: example.emarketingeye.net@PREVIEW_DOMAIN: $previewdomain@g" .gitlab-ci.yml
sed -i "s@PREVIEW_APP_NAME: example-emarketingeye-net@PREVIEW_APP_NAME: $previewappname@g" .gitlab-ci.yml

sed -i "s@www-example-com@$liveappname@g" docker-compose.yaml
sed -i "s@local.example.com@$localdomain@g" docker-compose.yaml

sed -i "s@WP_VERSION=version@WP_VERSION=$wpversion@g" .env
sed -i "s@PHP_VERSION=version@PHP_VERSION=$phpversion@g" .env
sed -i "s@php-version@php-$phpversion@g" .env

git add --all && git commit -m "Initial Commit" && git push origin develop && cd ..

