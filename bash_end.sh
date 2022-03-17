#!/bin/bash

ps -ef | grep gunicorn | grep -v grep | awk -F " " {'print $2;'} | xargs kill
