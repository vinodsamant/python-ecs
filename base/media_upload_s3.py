"""
file handling media upload s3 bucket
"""
# standard library
import os
import random
import string

# third-party
import boto
from boto.s3.key import Key
import boto3

from vier.settings import AWS_S3_CUSTOM_DOMAIN

AWS_ACCESS_KEY_ID = os.getenv('AWS_S3_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')


def upload_file_s3(**kwargs):
    """
    upload media file to s3
    bucket
    :return:
    :param kwargs:
    :return: file url from s3 bucket
    """
    media_file = kwargs["media_file"]
    s3 = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    ).resource('s3')
    s3_client = boto3.client('s3')
    file_new_name = str(file_name_creater()) + "." + str(
        media_file.name.split(".")[-1])
    s3_object = s3.Bucket(AWS_STORAGE_BUCKET_NAME).put_object(
        Key=str("profile-sp") + '/%s' % file_new_name,
        Body=media_file,
        ACL='public-read')
    return '%s/%s/%s' % (
        s3_client.meta.endpoint_url, AWS_STORAGE_BUCKET_NAME,
        s3_object.key)


def file_name_creater():
    """
    create alphanumeric with special character file name
    :return: string of length 32 characters
    """
    return "".join(
        [random.SystemRandom().choice(string.digits + string.ascii_letters)
         for _ in range(32)])


def upload_to_s3(file):
    """
    Uploads the given file to the AWS S3
    bucket and key specified.

    callback is a function of the form:

    def callback(complete, total)

    The callback should accept two integer parameters,
    the first representing the number of bytes that
    have been successfully transmitted to S3 and the
    second representing the size of the to be transmitted
    object.

    Returns boolean indicating success/failure of upload.
    """
    callback = None
    md5 = None
    reduced_redundancy = False
    content_type = None
    try:
        size = os.fstat(file.fileno()).st_size
    except (AttributeError, OSError):
        # Not all file objects implement fileno(),
        # so we fall back on this
        file.seek(0, os.SEEK_END)
        size = file.tell()

    conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(AWS_STORAGE_BUCKET_NAME, validate=True)
    k = Key(bucket)
    _, ext = os.path.splitext(file.name)
    k.key = str(file_name_creater()) + str(ext)
    if content_type:
        k.set_metadata('Content-Type', content_type)
    sent = k.set_contents_from_file(file, cb=callback, md5=md5,
                                    reduced_redundancy=reduced_redundancy,
                                    rewind=True)

    # Rewind for later use
    file.seek(0)

    if sent == size:
        return 'https://%s/%s' % (AWS_S3_CUSTOM_DOMAIN, k.key)
    return False
