#!/bin/bash

#set -Eeo pipefail

#trap "pipeline_notification 'fail' && exit 1" ERR
export PROFILE=default
export TERM=xterm-256color

if [[ -z "$1" ]]; then
    echo "You need to use this script with a parameter. (Either 'dev' or 'prod' for now)"
    exit 1
fi

echo "$1 pipeline started.."

export BUCKET=`aws ssm get-parameter --name /example/site-bucket/$1 --output text --query 'Parameter.Value' --profile $PROFILE`
export CLOUDFRONT=`aws ssm get-parameter --name /example/cf_distro/$1 --output text --query 'Parameter.Value' --profile $PROFILE`

npm install --silent --no-progress
npm run build
aws s3 sync build s3://$BUCKET  --profile $PROFILE
aws cloudfront create-invalidation --distribution-id $CLOUDFRONT --paths '/*'  --profile $PROFILE

echo "$1 Pipeline ended.."
