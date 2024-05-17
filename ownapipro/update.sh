zip ownapipro.zip lambda_function.py
aws lambda update-function-code --function-name ownapipro --zip-file fileb://ownapipro.zip
sleep 5
curl -X POST https://fx1zikyv5a.execute-api.eu-central-1.amazonaws.com/default/ownapipro -H 'Content-Type: application/json' -d '{"question":"co to jest prosty kat?"}'
