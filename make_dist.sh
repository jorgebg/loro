#!/bin/sh
rm /tmp/dist.zip

zip /tmp/dist.zip ./*.py
pushd ./venv/lib/python2.7/site-packages/
zip /tmp/dist.zip ./*
popd
