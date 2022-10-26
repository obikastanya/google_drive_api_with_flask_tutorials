from flask import Flask, request
from g_drive_service import GoogleDriveService

app=Flask(__name__)


service=GoogleDriveService().build()

@app.get('/all-files')
def get_all_files():
    
    
    selected_field="files(id, name, webViewLink)"

    
    return service.files().list(fields=selected_field).execute()



@app.get('/files-with-id/<file_id>/')
def get_files_with_id(file_id):
    selected_field="id, name, webViewLink"
    return service.files().get(
        fileId=file_id,
        fields=selected_field
    ).execute()

@app.get('/files-in-folder/<folder_id>/')
def get_files_in_folder(folder_id):
    
    selected_field="files(id, name, webViewLink, mimeType)"
    query=f" '{folder_id}' in parents "
    
    return service.files().list(
        q=query,
        fields=selected_field
    ).execute()

@app.get('/files-with-type')
def get_files_with_type():
    selected_mimetype=request.json.get("mimetype")
    folder_mimeType = 'application/vnd.google-apps.folder'
    
    selected_field="files(id, name, webViewLink, mimeType)"
    
    query=f"""
        mimeType != '{folder_mimeType}' 
        and 
        mimeType = '{selected_mimetype}' 
    """
    
    return service.files().list(
        q=query,
        fields=selected_field
    ).execute()
    


@app.get('/files-with-limit-offset')
def get_files_with_limit_offset():
    limit=request.args.get("limit")
    next_page_token=request.args.get("next_page_token")

    selected_field="nextPageToken, files(id, name, webViewLink)"
    
    result=service.files().list(
        pageSize=limit, 
        pageToken=next_page_token, 
        fields=selected_field
    ).execute()
    
    return result


@app.get('/files-with-limit-offset-order')
def get_files_with_limit_offset_order():
    limit=request.args.get("limit")
    next_page_token=request.args.get("next_page_token")

    selected_field="nextPageToken, files(id, name, webViewLink)"
    order_by="createdTime desc"
    
    result=service.files().list(
        pageSize=limit, 
        pageToken=next_page_token, 
        orderBy=order_by,
        fields=selected_field
    ).execute()
    
    return result


if __name__=='__main__':
    app.run(debug=True, port=8000)