# remotezip

The goal of this forked version of `remotezip` is to restrict some of the resources used before extracting.

This module provides a way to access single members of a zip file archive without downloading the full content from a remote web server. For this library to work, the web server hosting the archive needs to support the [range](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests) header. 

## Command line tool

This version of the project allows you to run the command line tool, `sremotezip.py`, with `docker-compose`. The flags and arguments can be passed during the build process using the host's environment variables.

```
FLAG=-l URL=url FILENAME=filename docker-compose up
```

The container will create and write the extracted files in a directory called `output`.

## Usage

### Initialization

`RemoteZip(url, ...)`

To download the content, this library rely on the `requests` module. The constructor interface matches the function `requests.get` module.

* **url**: Url where the zip file is located *(required)*.
* **auth**: authentication credentials.
* **headers**: headers to pass to the request.
* **timeout**: timeout for the request.
* **verify**: enable/disable certificate verification or set custom certificates location.
* ... Please look at the [requests](http://docs.python-requests.org/en/master/user/quickstart/#make-a-request) documentation for futher usage details.
* **initial\_buffer\_size**: How much data (in bytes) to fetch during the first connection to download the zip file central directory. If your zip file conteins a lot of files, would be a good idea to increase this parameter in order to avoid the need for further remote requests. *Default: 64kb*.

### Class Interface

`RemoteZip` is a subclass of the python standard library class `zipfile.ZipFile`, so it supports all its read methods:

* `RemoteZip.close()`
* `RemoteZip.getinfo(name)`
* `RemoteZip.extract(member[, path[, pwd]])`
* `RemoteZip.extractall([path[, members[, pwd]]])`
* `RemoteZip.infolist()`
* `RemoteZip.namelist()`
* `RemoteZip.open(name[, mode[, pwd]])`
* `RemoteZip.printdir()`
* `RemoteZip.read(name[, pwd])`
* `RemoteZip.testzip()`
* `RemoteZip.filename`
* `RemoteZip.debug`
* `RemoteZip.comment`

Please look at the [zipfile](https://docs.python.org/3/library/zipfile.html#zipfile-objects) documentation for usage details.


**NOTE**: `extractall()` and `testzip()` require to access the full content of the archive. If you need to use such methods, a full download of it would be probably more efficient.

### Examples

#### List members in archive

Print all members part of the archive:

```python
from remotezip import RemoteZip

with RemoteZip('http://.../myfile.zip') as zip:
    for zip_info in zip.infolist():
        print(zip_info.filename)
```


#### Download a member
The following example will extract the file `somefile.txt` from the archive stored at the url `http://.../myfile.zip`.

```python
from remotezip import RemoteZip

with RemoteZip('http://.../myfile.zip') as zip:
    zip.extract('somefile.txt')
```

#### S3 example

If you are trying to download a member from a zip archive hosted on S3 you can use the [aws-requests-auth](https://github.com/DavidMuller/aws-requests-auth) library for that as follow: 

```python
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from hashlib import sha256

auth = BotoAWSRequestsAuth(
    aws_host='s3-eu-west-1.amazonaws.com',
    aws_region='eu-west-1',
    aws_service='s3'
)
headers = {'x-amz-content-sha256': sha256('').hexdigest()}
url = "https://s3-eu-west-1.amazonaws.com/.../file.zip"

with RemoteZip(url, auth=auth, headers=headers) as z: 
    zip.extract('somefile.txt')
```

## How it works

This module uses the `zipfile.ZipFile` class under the hood to decode the zip file format. The `ZipFile` class is initialized with a file like object that will perform transparently the remote queries.

The zip format is composed by the content of each compressed member followed by the central directory.

How many requests will this module perform to download a member?

* If the full archive content is smaller than **initial\_buffer\_size**, only one request will be needed.
* Normally two requests are needed, one to download the central directory and one to download the archive member.
* If the central directory is bigger than **initial\_buffer\_size**, a third request will be required.

## Alternative modules

There is a similar module available for python [pyremotezip](https://github.com/fcvarela/pyremotezip).
