import os


def get_students(table):
    response = table.scan()
    data = list(response["Items"])
    while "LastEvaluatedKey" in response:
        response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
        data.extend(response["Items"])
    return data


def lambda_handler(event, context):
    import boto3

    table = boto3.resource("dynamodb").Table(os.getenv("STUDENT_TABLE", "Student-Details"))
    return get_students(table)
