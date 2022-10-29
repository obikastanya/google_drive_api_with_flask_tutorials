from flask import Flask
from g_drive_service import GoogleDriveService

app=Flask(__name__)
service=GoogleDriveService().build()

from apiclient import errors

@app.delete('/file/<file_id>/')
def delete_file(file_id):
    try:
        service.files().delete(fileId=file_id).execute()
        return {"status":"OK"}
    except errors.HttpError as error:
        return {"status":"Fail", "error_message":error.reason}
    except Exception as e:
        return {"status":"Fail", "error_message":str(e)}
     

if __name__=='__main__':
    app.run(debug=True, port=8000)