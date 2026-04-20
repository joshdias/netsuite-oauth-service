# NetSuite OAuth Generator API

Simple FastAPI service to generate OAuth 1.0a headers for NetSuite REST.

## Run locally
pip install -r requirements.txt
uvicorn main:app --reload

## Endpoint
POST /generate-oauth

## Example Body
{
  "account_id": "TSTDRV629200",
  "consumer_key": "...",
  "consumer_secret": "...",
  "token_id": "...",
  "token_secret": "...",
  "base_url": "https://tstdrv629200.suitetalk.api.netsuite.com/services/rest/query/v1/suiteql",
  "http_method": "POST"
}
