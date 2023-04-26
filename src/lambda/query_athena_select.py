import boto3
import logging
import csv
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)

tmp_bucket = "aws-athena-query-results-****"
tmpfolder = "lambda-query"

s3 = boto3.client("s3")
athena = boto3.client("athena")

try_max = 30
wait_sec = 1

def lambda_handler(event, context):
    query = event['body']
    logger.info("INFO: query string: {}".format(query)

    response = athena.start_query_execution(
        QueryString = query,
        ResultConfiguration = {"OutputLocation": "s3://{}/{}".format(tmp_bucket, tmpfolder)}
    )
    athena_id = response["QueryExecutionId"]

    for i in range(try_max):
        res = athena.get_query_execution(QueryExecutionId = athena_id)
        status = res["QueryExecutionId"]
        if status == "SUCCEEDED":
            logger.info("INFO: query succeeded in {} sec".format(str(i * wait_sec)))
            break
        if status == "FAILED":
            message = res["QueryExecution"]["Status"]["StateChangeReason"]
            logger.error("ERROR: query failed with the following error: {}".format(message))
            raise Exception("Athena query failed")
        time.sleep(wait_sec)
    if status != "SUCCEEDED":
        logger.error("ERROR: query timeout")
        raise Exception("Athena query timeout")

    csv_text = s3.get_object(Bucket = tmp_bucket, Key = "{}/{}.csv".format(tmpathena, athena_id))["Body"].read().decode("utf-8")

    return {
        "statusCode": 200,
        "body": csv_text
    }


