import json
import logging
import os

import boto3

import make_decision.helper as helper


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger = logging.getLogger()
    logger.info("store check")
    payload_body = json.loads(event["body"])
    data = {
        "value": {
            "message": "Seventh level",
            "vendor": "none",
            "topics": payload_body["metadata"]["topics"],
            "borrower_data": {
                "full_data": payload_body,
            },
        }
    }
    data["value"]["borrower_data"]["decision"] = payload_body["metadata"]["decision"]
    # TODO: This is an incorrect data model. I mapped to for the time being.
    # This needs to be simplified.
    # fix data model first
    # data = zventus_blockchain.data_model.decision(**data)

    if "kaleido.io" in os.environ["FIREFLY_SERVER"]:
        firefly_receiver = "u0t9q1a0v9"
    else:
        firefly_receiver = "did:firefly:node/node_7182f1"

    response = helper.call_chain(
        data=data,
        tag="decision_in_chain",
        receiver=firefly_receiver,
        topics=payload_body["metadata"]["topics"],
    )
    response["employment_verified"] = True
    filtered_response = {
        key: response[key] for key in ["employment_verified", "data", "hash", "header"]
    }

    client = boto3.resource("dynamodb")

    # this will search for dynamoDB table
    # your table name may be different
    table = client.Table("load_data_2")

    a, v = helper.get_update_params({"decision": payload_body["metadata"]["decision"]})
    table.update_item(
        Key={"loan_data": str(payload_body["metadata"]["topics"])},
        UpdateExpression=a,
        ExpressionAttributeValues=dict(v),
    )

    return {
        "statusCode": 200,
        "body": json.dumps(filtered_response),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Allow": "GET, OPTIONS, POST",
            "Access-Control-Allow-Methods": "GET, OPTIONS, POST",
            "Access-Control-Allow-Headers": "*",
        },
    }


#############################################
