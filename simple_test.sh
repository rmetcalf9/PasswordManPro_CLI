#!/bin/bash

passwordmanpro_cli rawget /restapi/json/v1/resources
RES=$?
if [[ ${RES} -ne 0 ]]; then
  echo "ERROR CODE RETURNED - $RES"
else
  echo "OK"
fi
