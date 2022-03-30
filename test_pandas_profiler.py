from pandas_profiling import ProfileReport

import boto3
import awswrangler as wr
import re


def profile_data(event, runs):
    # file_path = event[0]
    s3 = boto3.resource("s3")
    bucket = s3.Bucket('fast-data-qa')
    df = wr.s3.read_parquet(path='s3://fast-data-qa/data/housing/housing.parquet')
    profile = ProfileReport(df, title="Pandas Profiling Report", minimal=True)
    report = profile.to_html()
    match = re.search('.+(\/)(.*?).parquet', "data/housing/housing.parquet")
    match_root_file_name = re.search('[^_]*', match.group(2))
    folder = match_root_file_name.group(0) + '/'
    links_result = []
    for obj in bucket.objects.filter(Prefix=folder):
        if obj.size: links_result.append("https://d35b8h21obf2t9.cloudfront.net/" + str(obj.key))
    objs = list(bucket.objects.filter(Prefix=folder))
    key = 0
    if len(objs) > 0 and objs[0].key == folder:
        folders = []
        client = boto3.client('s3')
        result = client.list_objects(Bucket='fast-data-qa', Prefix=folder, Delimiter='/')

        for o in result.get('CommonPrefixes'):
            folders.append(str(o.get('Prefix')).replace(folder, '').replace('/', ''))
        key = int(folders[-1]) + 1
        folder = folder + str(key) + '/'
        bucket.put_object(Key=folder)
    else:
        bucket.put_object(Key=folder)
        folder = folder + '0/'
        bucket.put_object(Key=folder)

    bucket.put_object(Key=folder + match.group(2) + '.html', Body=report, ContentType='text/html')
    if runs > 1:
        bucket.put_object(Key=folder + 'skip.txt', Body='')
    # for i in range(runs):
    links_result.append("https://d35b8h21obf2t9.cloudfront.net/" + folder + match.group(2) + ".html")

    return links_result
