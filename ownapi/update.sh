zip ownapi.zip lambda_function.py
aws lambda update-function-code --function-name ownapi --zip-file fileb://ownapi.zip
sleep 5
curl -X POST https://fx1zikyv5a.execute-api.eu-central-1.amazonaws.com/default/ownapi -H 'Content-Type: application/json' -d '{"question":"co to jest kwadrat?"}'
