"""
Enforces storage strategies. E.g. all files related to patient referral
would be stored in bucketname/candidate-docs/ etc.
"""

from storages.backends.s3boto3 import S3Boto3Storage


class MediaStorage(S3Boto3Storage):
    location = 'media/'
    file_overwrite = False
    default_acl = 'private'
