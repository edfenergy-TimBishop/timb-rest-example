#!/bin/bash

#set -Eeo pipefail

#trap "pipeline_notification 'fail' && exit 1" ERR
export AWS_PROFILE=default
export APP="example"
export STAGE=$1
export TERM=xterm-256color

if [[ -z "$STAGE" ]]; then
    echo "You need to use this script with a parameter. (Either 'dev' or 'prod')"
    exit 1
fi


echo "$STAGE pipeline started.."

sls deploy --stage $STAGE

echo "$STAGE Pipeline ended.."