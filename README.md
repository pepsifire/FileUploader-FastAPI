# FileUploader-FastAPI

- Fileuploader using FastAPI as the backend
- ShareX supported

## Todo
- [x] Make allowed content modifiable via environment variables
- [x] Toggleable random filenames
- [ ] File deletion
- [ ] Admin menu (File deletion)

## Docker deployment

| Environment variables | Meaning |
|----------|---------| 
| auth_user  | HTTP Basic username |
| auth_password  | HTTP Basic password |
| base_url | Base url WITHOUT trailing slash |
| allowed_content_types | List of allowed MIME types |

## Note
- If no environment values are supplied the defaults are:
    - auth_user=1234
    - auth_password=1111
    - base_url=http://localhost:8000
