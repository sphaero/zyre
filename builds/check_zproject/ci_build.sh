#!/usr/bin/env bash
set -ex

git clone --quiet --depth 1 https://github.com/zeromq/libzmq libzmq
git clone --quiet --depth 1 https://github.com/zeromq/czmq czmq

docker run -v "$REPO_DIR":/gsl zeromqorg/zproject project.xml

# keep an eye on git version used by CI
git --version
if [[ $(git --no-pager diff -w) ]]; then
    git --no-pager diff -w
    echo "There are diffs between current code and code generated by zproject!"
    exit 1
fi
if [[ $(git status -s) ]]; then
    git status -s
    echo "zproject generated new files!"
    exit 1
fi
