#!/bin/bash

#set -Eeo pipefail

#trap "pipeline_notification 'fail' && exit 1" ERR
export AWS_PROFILE=default
export APP="example"
export STAGE=$1
export TERM=xterm-256color

if [[ -z "$STAGE" ]]; then
    echo "You need to use this script with a parameter. (Either 'dev' or 'prod' or 'bootstrap')"
    exit 1
fi

rm -Rf terraform/.terraform

if [ "$STAGE" == "bootstrap" ]; then
    cd terraform
    terraform init
    terraform workspace new dev
    terraform workspace new prod
    cd ..
else
    echo "$STAGE pipeline started.."

    # Common components
    echo "Common components build and deploy stage"
    cd terraform
    terraform init
    terraform workspace select $STAGE
    terraform apply -auto-approve
    cd ..

    echo "$STAGE Pipeline ended.."
fi