import json
import os
import uuid
from datetime import datetime, timezone, timedelta


def add_student(event, table):
    try:
        fields = {key: str(event[key]).strip() for key in ("roll_number", "student_name", "student_class")}
        if any(not value or len(value) > 200 for value in fields.values()) or fields["student_class"] == "Select":
            raise ValueError("Invalid fields")
    except (KeyError, TypeError, ValueError):
        return {"statusCode": 400, "body": json.dumps("Invalid student details")}
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    table.put_item(Item={
        "ID": str(uuid.uuid4()), **fields,
        "LatestGreetingTime": now.strftime("%a, %d %b %Y %H:%M:%S +0530 IST"),
    })
    return {"statusCode": 200}


def lambda_handler(event, context):
    import boto3

    table = boto3.resource("dynamodb").Table(os.getenv("STUDENT_TABLE", "Student-Details"))
    try:
        return add_student(event, table)
    except Exception:
        return {"statusCode": 500, "body": json.dumps("Unable to save student")}
