import boto3
import pandas as pd
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource("dynamodb")

# Busqueda en organization

table = dynamodb.Table("nita_organizations")
response = table.scan(
    FilterExpression="contact_name = :value",
    ExpressionAttributeValues={":value": "Fantasma Jr"},
    ProjectionExpression="contact_name, contact_email, contact_phone_number, organization_name, organization_id",
)

items = response["Items"]

organization_id = items[0].pop("organization_id")
df = pd.DataFrame(items)
df.to_excel("data_organization.xlsx", sheet_name="data_org", index=False)

# Busqueda en assessment

table = dynamodb.Table("nita_assessment")
response = table.scan(
    FilterExpression="organization_id = :value",
    ExpressionAttributeValues={":value": organization_id},
    ProjectionExpression="answers",
)

data = response["Items"][0]["answers"]

for key, value in data.items():
    value_copy = value.copy()
    for k, v in value.items():
        if v == False:
            value_copy.pop(k)
    df = pd.DataFrame(value_copy, index=value.keys())
    df = df.head(1)
    with pd.ExcelWriter(
        "data_organization.xlsx", engine="openpyxl", mode="a"
    ) as writer:
        df.to_excel(writer, sheet_name=key.replace("/", "-")[:30], index=False)

# table = dynamodb.Table("nita_assessment")
# response = table.scan(
#     FilterExpression="answers.#web_movile.#web > :value",
#     ExpressionAttributeNames={"#web_movile": "Web o movil", "#web": "web"},
#     ExpressionAttributeValues={":value": 10},
#     ProjectionExpression="answers",
# )

# items = response["Items"]
# print(items)
# print(items[0]["answers"]["Web o movil"]["web"])
