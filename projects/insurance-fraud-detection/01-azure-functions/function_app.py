import azure.functions as func
import json
import logging
from azure.storage.filedatalake import DataLakeServiceClient
from datetime import datetime
import hashlib

app = func.FunctionApp()

# Initialize Azure Data Lake Storage client
def get_adls_client(connection_string):
    return DataLakeServiceClient.from_connection_string(connection_string)

def get_file_path(event_type, date_str):
    """Generate hierarchical path: /raw/{event_type}/{YYYY}/{MM}/{DD}/{HH}"""
    return f"raw/{event_type}/{date_str[:4]}/{date_str[5:7]}/{date_str[8:10]}/{date_str[11:13]}"

def deduplicate_event(event_data):
    """Create hash of key fields to detect duplicates"""
    key_string = f"{event_data.get('policy_id')}{event_data.get('claim_id')}{event_data.get('timestamp')}"
    return hashlib.md5(key_string.encode()).hexdigest()

@app.function_name("IngestPolicyUpdates")
@app.route_trigger(route="ingest-policy", methods=["POST"])
def ingest_policy_updates(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function triggered by HTTP POST from CP platform
    Captures policy updates and stores in ADLS Gen2 Bronze layer
    """
    
    logging.info("Policy update ingestion triggered")
    
    try:
        # Get request body
        req_body = req.get_json()
        event_type = req_body.get('event_type')  # policy_created, policy_updated, claim_filed
        
        if not event_type:
            return func.HttpResponse("Missing event_type", status_code=400)
        
        # Add metadata
        req_body['ingestion_timestamp'] = datetime.utcnow().isoformat()
        req_body['event_hash'] = deduplicate_event(req_body)
        req_body['source_system'] = 'CP_PLATFORM'
        
        # Get ADLS connection
        connection_string = os.environ.get('ADLS_CONNECTION_STRING')
        client = get_adls_client(connection_string)
        
        # Get file system and directory
        file_system_client = client.get_file_system_client('insurance-raw')
        date_str = datetime.utcnow().isoformat()
        file_path = get_file_path(event_type, date_str)
        
        # Create directory if not exists
        directory_client = file_system_client.get_directory_client(file_path)
        try:
            directory_client.create_directory()
        except:
            pass  # Directory already exists
        
        # Create file name with timestamp and event_hash (prevents duplicates)
        file_name = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}__{req_body['event_hash'][:8]}.json"
        
        # Write to ADLS
        file_client = directory_client.get_file_client(file_name)
        file_client.upload_file(
            data=json.dumps(req_body, indent=2),
            overwrite=True
        )
        
        logging.info(f"Stored event: {event_type} to {file_path}/{file_name}")
        
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "event_type": event_type,
                "file_path": f"{file_path}/{file_name}",
                "timestamp": req_body['ingestion_timestamp']
            }),
            status_code=202,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in ingest_policy_updates: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )


@app.function_name("IngestClaimUpdates")
@app.route_trigger(route="ingest-claim", methods=["POST"])
def ingest_claim_updates(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function for capturing claim filings and updates
    Similar structure to IngestPolicyUpdates but for claim events
    """
    
    logging.info("Claim update ingestion triggered")
    
    try:
        req_body = req.get_json()
        
        # Validate required fields
        required_fields = ['claim_id', 'policy_id', 'claim_amount', 'claim_date']
        if not all(field in req_body for field in required_fields):
            return func.HttpResponse(
                json.dumps({"error": f"Missing required fields: {required_fields}"}),
                status_code=400,
                mimetype="application/json"
            )
        
        # Add metadata
        req_body['ingestion_timestamp'] = datetime.utcnow().isoformat()
        req_body['event_hash'] = deduplicate_event(req_body)
        req_body['source_system'] = 'CP_PLATFORM'
        
        # Store in ADLS
        connection_string = os.environ.get('ADLS_CONNECTION_STRING')
        client = get_adls_client(connection_string)
        file_system_client = client.get_file_system_client('insurance-raw')
        
        date_str = datetime.utcnow().isoformat()
        file_path = get_file_path('claims', date_str)
        
        directory_client = file_system_client.get_directory_client(file_path)
        try:
            directory_client.create_directory()
        except:
            pass
        
        file_name = f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}__{req_body['event_hash'][:8]}.json"
        file_client = directory_client.get_file_client(file_name)
        file_client.upload_file(
            data=json.dumps(req_body, indent=2),
            overwrite=True
        )
        
        logging.info(f"Claim stored: {file_path}/{file_name}")
        
        return func.HttpResponse(
            json.dumps({
                "status": "success",
                "claim_id": req_body.get('claim_id'),
                "file_path": f"{file_path}/{file_name}"
            }),
            status_code=202,
            mimetype="application/json"
        )
        
    except Exception as e:
        logging.error(f"Error in ingest_claim_updates: {str(e)}")
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
