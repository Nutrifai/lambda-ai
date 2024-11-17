from dataclasses import dataclass
from Entities.Tables.base_table import Table
from env.ddb_client import get_ddb_client
from boto3.dynamodb.conditions import Key

@dataclass
class TableRepository:
    table: Table
    
    def __post_init__(self):
        self.__dynamo_table_instance = get_ddb_client().Table(self.table.name)

    @property
    def __dynamo_table(self):
        return self.__dynamo_table_instance

    def get_all(self, filters = None):
        params = {}

        if filters:
            params["FilterExpression"] = filters

        scan_response = self.__dynamo_table.scan(**params)

        return scan_response["Items"]
    
    def get_by_pk(self, pk, sk=""):
        filters = Key(self.table.partition_key).eq(pk)

        if sk and self.table.sort_key:
            filters = filters & Key(self.table.sort_key).eq(sk)


        query = self.__dynamo_table.query(
            KeyConditionExpression=filters
        )

        return query["Items"]

    def create_item(self, body):
        item = self.table.model(**body).model_dump()
        
        self.__dynamo_table.put_item(Item=item)

        pk = item[self.table.partition_key]
        sk = "" if not self.table.sort_key else item[self.table.sort_key]

        return self.get_by_pk(pk, sk)
    

    def delete_item(self, pk, sk=""):
        if self.table.sort_key and not sk:
            raise Exception(f"Should use Partition Key and Sort Key for table {self.table.name}")
        
        key = {self.table.partition_key: pk}
        
        if sk and self.table.sort_key:
            key[self.table.sort_key] = sk
        
        delete_response = self.__dynamo_table.delete_item(Key=key)
        
        return {
            "operationStatus": delete_response.get("ResponseMetadata", {}).get("HTTPStatusCode")
        }
    
    def update_item(self, pk, sk="", new_values = {}):
        if self.table.sort_key and not sk:
            raise Exception(f"Should use Partition Key and Sort Key for table {self.table.name}")
        
        if (
            self.table.partition_key in new_values and pk != str(new_values.get(self.table.partition_key, ""))
            or self.table.sort_key in new_values and sk != str(new_values.get(self.table.sort_key, ""))
        ):

            raise ValueError(
                f"the value of partition_key '{self.table.partition_key}'"
                f"{' or sort_key ' + self.table.sort_key if self.table.sort_key else ''} "
                f"in the body is different from partition_key '{pk}'"
                f"{' or sort_key ' + sk if self.table.sort_key else ''} "
                "present in request path"
            )


        current_value = self.get_by_pk(pk, sk)

        if not current_value:
            raise Exception(f"Item with pk: {pk} and sk: {sk} not found")

        updated_item = self.table.model(
            **{
                **current_value[0],
                **new_values
            }
        )

        self.__dynamo_table.put_item(Item=updated_item.model_dump())

        return self.get_by_pk(pk, sk)