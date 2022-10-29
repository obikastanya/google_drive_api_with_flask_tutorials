from flask import Flask, request, jsonify
from g_drive_service import GoogleDriveService

app=Flask(__name__)
service=GoogleDriveService().build()

from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload
from datetime import datetime

@app.post('/upload')
def upload_file():
    
    uploaded_file=request.files.get("file")

    buffer_memory=BytesIO()
    uploaded_file.save(buffer_memory)

    media_body=MediaIoBaseUpload(uploaded_file, uploaded_file.mimetype, resumable=True)
    created_at= datetime.now().strftime("%Y%m%d%H%M%S")
    file_metadata={
        "name":f"{uploaded_file.filename} ({created_at})"
    }

    returned_fields="id, name, mimeType, webViewLink, exportLinks"
    
    upload_response=service.files().create(
        body = file_metadata, 
        media_body=media_body,  
        fields=returned_fields
    ).execute()

    return upload_response


 
if __name__=='__main__':
    app.run(debug=True, port=8000)