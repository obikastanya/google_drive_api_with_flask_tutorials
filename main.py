from flask import Flask, request
from g_drive_service import GoogleDriveService

app=Flask(__name__)


service=GoogleDriveService().build()

@app.post('/upload')
def upload_file():
    pass
 
if __name__=='__main__':
    app.run(debug=True, port=8000)