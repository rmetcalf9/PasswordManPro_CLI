#!/bin/bash

echo 'To test one file pass filename as first param'
echo 'e.g. sudo ./continous_test.sh test_JobExecution.py'

if [ $# -eq 0 ]; then
  until ack -f --python  ./passwordmanpro_cli ./tests | entr -d nosetests --rednose ./tests; do sleep 1; done
else
  until ack -f --python  ./passwordmanpro_cli ./tests | entr -d nosetests --rednose ./tests/${1}; do sleep 1; done
fi
