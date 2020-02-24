#!/bin/bash

up() {
    git clone -b pipeline --single-branch git@github.com:guzman-raphael/djhub.git
    # git clone -b master --single-branch git@github.com:guzman-raphael/djhub.git
    # git clone -b update_schema --single-branch git@github.com:guzman-raphael/djhub.git
    if [ "$1" = "LOCAL" ]; then
        env $(cat LNX.env;echo;cat common.env;echo;cat private.env) \
            docker-compose -f local-docker-compose.yml up --build
    elif [ "$1" = "TRAVIS" ]; then
        env $(cat common.env) \
            docker-compose -f LNX-docker-compose.yml up --build --exit-code-from app
    fi
}

down() {
    if [ "$1" = "LOCAL" ]; then
        env $(cat LNX.env;echo;cat common.env;echo;cat private.env) \
            docker-compose -f local-docker-compose.yml down
    elif [ "$1" = "TRAVIS" ]; then
        env $(cat common.env) \
            docker-compose -f LNX-docker-compose.yml down
    fi
    sudo rm -R djhub
}

"$@"