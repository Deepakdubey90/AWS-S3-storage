from flask import Flask,render_template, request
import boto3,botocore

#AWS secret credentials
aws_access_key_id = '###'
aws_secret_access_key = '###'
region='us-east-2'

#connecting to s3
s3=boto3.resource(service_name='s3', aws_access_key_id=aws_access_key_id,
aws_secret_access_key=aws_secret_access_key,region_name=region)
print 'connected to Amazon simple storage service'

#Initializing bucket_name
bucket_name='namratha'


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
    #return app.send_static_file('home.html')

ALLOWED_EXTENSIONS = set(['jpg','png'])

def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload')
def upload():
    filename=request.args.get('file')
    filepath='/home/ubuntu/flaskapp/'+filename
    data = open(filepath, 'rb')
    s3.Bucket(bucket_name).put_object(Key=filename, Body=data)
    return 'File uploaded!'

@app.route('/download')
def download():
    filename=request.args.get('filename')
    try:
        s3.Bucket(bucket_name).download_file(filename, 'hello1.txt')
        # hello1.txt is the filename u want the downloading file to be named as.. It can be diff from the file on cloud
        return 'File downloaded successfully'
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object key i.e file does not exist.")

@app.route('/listbucket')
def listbucket():
    s = ''
    for bucket in s3.buckets.all():
        s += bucket.name + ","
    return render_template('display buckets.html',output=s)

@app.route('/listfiles')
def listfiles():
    for bucket in s3.buckets.all():
        for key in bucket.objects.all():
            print '{0} - {1}'.format(bucket.name, key.key)
    #prints in the format: Bucket Name - Object Key Name

@app.route('/delete')
def delete():
    filename=request.args.get('filename')
    s3.Object(bucket_name, filename).delete()
    return 'File deleted'