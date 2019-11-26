### Official Alpha Vantage Chainlink external adapter for python 3+

Full documentation for Alpha Vantage can be found [here](https://www.alphavantage.co/documentation/)

**Adapter Formats**: Google Cloud Function, AWS Lambda and Docker

**All Endpoints (functions) supported** 

## Cloud Installation:
Make the bash script executable

```chmod +x ./create_zip.bsh```

Create the adapter zip for your cloud provider ( gcs or aws )

```./create_zip.bsh aws```

Upload the created zip to your provider and set the appropriate handler ( gcs_handler or aws_handler ) to be triggered by a HTTP event.

Create an ALPHAVANTAGE_API_KEY environment variable and set it to your Alpha Vantage API key
You can get one [here](https://www.alphavantage.co/support/#api-key)

## Docker Installation:
Build the image
```
docker build -t alpha-vantage-cl-ea .
```
Run the container while passing in your ALPHAVANTAGE_API_KEY
```
docker run -e ALPHAVANTAGE_API_KEY=************** -p 5000:5000 alpha-vantage-cl-ea
```
The adapter endpoint will be accessable from ```http://localhost/:5000/alpha-vantage-cl-ea```

## Sample call:
```
curl -X POST "https://us-central1-chainlink-256615.cloudfunctions.net/function-1" -H "Content-Type:application/json" --data '{"data": {"function":"GLOBAL_QUOTE", "symbol":"TSLA"}}'
```
Sample return:
```
{
  "jobRunID": "", "data": {
  "Global Quote": {
    "01. symbol": "TSLA", 
    "02. open": "319.6200", 
    "03. high": "323.5000", 
    "04. low": "316.1180", 
    "05. price": "317.2200", 
    "06. volume": "6615477", 
    "07. latest trading day": "2019-11-05", 
    "08. previous close": "317.4700", 
    "09. change": "-0.2500", 
    "10. change percent": "-0.0787%"}
    }, 
  "status": "200"
}
```

## Sample Web Job Spec
```
{
  "initiators": [
    {
      "type": "web",
      "params": {
      }
    }
  ],
  "tasks": [
    {
      "type": "alpha-vantage-cl-ea,
      "confirmations": 0,
      "params": {
        "function": "GLOBAL_QUOTE",
        "symbol": "MSFT"
      }
    }
  ],
  "startAt": null,
  "endAt": null
```

## Sample Job Spec
```
{
  "initiators": [
    {
      "type": "runlog",
      "params": {
        "address": "0xb36d3709e22f7c708348e225b20b13ea546e6d9c"
      }
    }
  ],
  "tasks": [
    {
      "type": "alpha_vantage_cl_ea",
      "confirmations": null,
      "params": {
      }
    },
    {
      "type": "copy",
      "confirmations": null,
      "params": {
      }
    },
    {
      "type": "multiply",
      "confirmations": null,
      "params": {
      }
    },
    {
      "type": "ethint256",
      "confirmations": null,
      "params": {
      }
    },
    {
      "type": "ethtx",
      "confirmations": null,
      "params": {
      }
    }
  ],
  "startAt": null,
  "endAt": null
}
```

Full documentation for Alpha Vantage can be found [here](https://www.alphavantage.co/documentation/)

## Testing

To test just the URL creation run:
```python -m pytest -k test_url_creation```

Once you have ```test_config.json``` set up, you can run each appropriatly depending on your setup.

If you have a docker, aws, and gcp setup, feel free to run:
```python -m pytest```

```test_data.json``` contains example payloads for some supported endpoints, paths and their parameters.

