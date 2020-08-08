# Тестовое задание
## API Usage

### Adding new image
Add an image by sending a base64 encoded image. On correct encoding, the image will be decoded with a basic integrity check (openable by ```Pillow```). Name of this image will be asigned randomly.
###### Request:
```
POST /image

R0lGODlhEAAOALMAAOazToeHh0tLS/7LZv/0j
vb29t/f3//Ub//ge8WSLf/rhf/3kdbW1mxsbP//mf///yH5BAAAAAAALAAAAAAQAA4AAA
Re8L1Ekyky67QZ1hLnjM5UUde0ECwLJoExKcppV0aCcGCmTIHEIUEqjgaORCMxIC6e0Cc
guWw6aFjsVMkkIr7g77ZKPJjPZqIyd7sJAgVGoEGv2xsBxqNgYPj/gAwXEQA7
```
###### Response:
```
200 OK
Content type: application/json

{
    "new_image_filename": "gkzexxdkps.jpg",
    "success": true
}
```

### Listing images
Returns a list of stored image with background data:
* file name as ```file_name```
* last modification time in UNIX timestamp format as ```last_modification_time```
* file size in bytes as ```size```
###### Request:
```
GET /image
```
###### Response:
```
200 OK
Content type: application/json

[
    {
        "file_name": "gkzexxdkps.jpg",
        "last_modificaion_time": 1596880380.1825516,
        "size": 120223
    },
    {
        "file_name": "asdfdfasdf.jpg",
        "last_modificaion_time": 1596880380.1825516,
        "size": 767123
    }
]
```

### Deleting images
Deletes an image with the name provided in request. If file extension is not provided, will delete all files with the same name of all supported extensions.
###### Request:
```
DELETE /image

gkzexxdkps.jpg
```
###### Response:
```
200 OK
Content type: application/json

{
    "deleted_filename": "gkzexxdkps.jpg",
    "success": true
}
```

### Retrieving an image
Get an image by provided filename, returns image file
###### Request:
```
GET /images/<image name>.jpg
```
###### Response:
```
Content type: image/jpeg
```

## Configuration
By default, the only supported extension is ```.jpg```. Can be further extended to support more extensions, such as ```.png .jpeg```, etc. This can be done in ```config.py``` in root project directory.

Directory to store images can also be set in ```config.py``` file. For testing scenario, it is possible to configure app to automatically remove this folder on unittest teardown.

## Deployment
Run ```$docker-compose up``` in project directory. By default uses port ```5000```

## Testing
Run ```$flask run``` to start provided basic unit tests and a full usage scenario.

## Dependencies
Docker: based on ```tiangolo/uwsgi-nginx-flask:python3.7``` image
python: ```Flask```, ```Pillow``` (see details in ```requirements.txt```)
