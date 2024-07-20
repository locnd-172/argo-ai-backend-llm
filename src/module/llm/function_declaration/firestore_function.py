firestore_function_declaration = {
    "name": "get_firestore_data",
    "description": "Retrieves data from Firestore 'mrv_system' collection based on provided filters.",
    "parameters": {
        "type": "object",
        "properties": {
            "filters": {
                "type": "array",
                "description": "A list of filters (field, operator, value) to apply to the query. The filter fields are 'facility', 'date', 'plant', 'metrics'.",
                "items": {
                    "type": "object",
                    "description": "A dictionary of filters (field, operator, value) to indicate a filter to be applied to the query.",
                    "properties": {
                        "field": {
                            "type": "string",
                            "description": "field name of filter item"
                        },
                        "operator": {
                            "type": "string",
                            "description": "operator of filter item, one of following: `==`, `>=`, `<=`. Default operator is `==`"
                        },
                        "value": {
                            "type": "string",
                            "description": "value of filter item"
                        }
                    }
                }
            }
        },
        "required": ["filters"]
    }
}
