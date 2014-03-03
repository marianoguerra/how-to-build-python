#!/usr/bin/env sh
set -e
for release in $(cat supported-ubuntu-releases)
do
    sudo lxc-create -t ubuntu -n py-build-$release -- -r $release
done
