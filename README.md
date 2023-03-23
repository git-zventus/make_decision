# Blockchain POC

## AWS Lambda function code

Under zventus_blockchain we have a poetry installable package that will be packaged and uploaded to the lambda function we will be using for poc V2.

## Packaging the lambda function

If you want to install this repository locally using Poetry (which has to be already installed) run the following command:

```bash
make install
```

and if you want to zip it

```bash
make zip_lambda
```

You can then upload this artifact.zip into AWS. Ideally you setup a GitHub action to do all the steps above and even uploading it to lambda automatically after passing some unit tests to make sure the new version is not broken.

There are additinal instructions for formatting the code 


```bash
make format
```