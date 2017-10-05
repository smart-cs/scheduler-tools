#!/bin/bash
PY_SOURCE="../../lambda_handler.py ../../course.py ../../schedulecreator.py"
OUTPUT_ZIP="../../returnSchedule.zip"
AWS_FUNCTION_NAME="returnSchedule"

hash 7z 2>/dev/null || { echo >&2 "Requires '7z' to be in PATH to zip files (may need to install or add to PATH). Aborting..."; exit 1; }

cd Lib/site-packages/
echo "rm -rf $OUTPUT_ZIP"
rm -rf $OUTPUT_ZIP
echo "7z a $OUTPUT_ZIP * $PY_SOURCE -xr!__pycache__"
7z a $OUTPUT_ZIP * $PY_SOURCE -xr!__pycache__

hash aws 2>/dev/null || { echo >&2 "Requires 'aws' to be in PATH to deploy to aws lambda (may need to install or add to PATH)."; exit 1; }
echo "aws lambda update-function-code --function-name $AWS_FUNCTION_NAME --zip-file fileb://$OUTPUT_ZIP"
aws lambda update-function-code --function-name $AWS_FUNCTION_NAME --zip-file fileb://$OUTPUT_ZIP
