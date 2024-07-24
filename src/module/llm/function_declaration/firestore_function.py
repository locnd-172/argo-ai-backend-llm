firestore_function_declaration = {
    "name": "get_report_data",
    "description": "Retrieves report data of a farm from Firestore 'mrv_system' collection based on provided input data.",
    "parameters": {
        "type": "object",
        "properties": {
            "facility": {
                "type": "string",
                "description": "Farm name or field name that user is inquiring for report. Return default `DEF_VALUE` if not mentioned",
            },
            "date": {
                "type": "string",
                "description": "Report date in dd/MM/yyyy format. Return default `DEF_VALUE` if not mentioned",
            },
            "metrics": {
                "type": "string",
                "description": "Metrics field to retrieve data for, some of following: `irrigation`, `weather`, `pest`, `soil`. Return default `DEF_VALUE` if not mentioned"
            }
        },
        "required": ["facility", "date"]
    }
}
