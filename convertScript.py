# export DJANGO_SETTINGS_MODULE=cloudprojects.settings
import boto3
import manage
import django
import subprocess
import datetime
import os
import smtplib
from botocore.exceptions import ClientError

os.environ.setdefault("DJANGO_SETTINGS_MODULE","cloudprojects.settings")


import random
import string


django.setup()
from project1.models import Video

s3 = boto3.resource('s3')


#q = list(Video.objects(estado="Pendiente"))
# subprocess.call('ls')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/cloudprojects/media/'

url = ' media/videosPublicados/'
name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
# fsa.join()
print(BASE_DIR)

sender = "pruebascloud2017@gmail.com"

#configSet = "ConfigSet"

awsregion = "us-west-2"

subject = "SmartTools Video"

# The email body for recipients with non-HTML email clients.  
textbody = "\n El video ha sido publicado exitosamente!"

# The character encoding for the email.
charset = "UTF-8"

# Create a new SES resource and specify a region.
client = boto3.client('ses',region_name=awsregion)
sqs = boto3.resource('sqs',region_name=awsregion)
queue = sqs.get_queue_by_name(QueueName='videosToConvert.fifo')
q  = queue.receive_messages(
    MaxNumberOfMessages=5,
)

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login('pruebascloud2017@gmail.com', 'cloud2017')
msg = '\n El video ha sido publicado exitosamente!'

for Q in q:
    print('\n')
    url = 'videosPublicados/'
    s3.meta.client.download_file('smarttoolsg12', 'videosSubidos/{}'.format(Q.body), BASE_DIR + Q.body)
    name = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    # command = 'cp .' + Q.videoSubido.url+ ' ' + url
    command = 'ffmpeg -i ' + BASE_DIR + Q.body + ' -c:a aac -strict -2 -c:v libx264 ' + BASE_DIR + url+name+'_'+date+'.mp4'
    video = Video.objects.get(videoSubido=Q.body)

    try:
        print(command)
        # subprocess.call(command)
        filename = name+'_'+date+'.mp4'
        os.system(command)
        s3.meta.client.upload_file(BASE_DIR + url+name+'_'+date+'.mp4', 'smarttoolsg12', 'videosPublicados/{}'.format(filename))
        video.videoPublicado = filename
        video.estado ='Convertido'
        video.save()
        Q.delete()
    except Exception as e:
        # raise
        print('Error ' + video.videoSubido)
        print('\n')
        print(e)
    else:
        print('Convertido ' + url+name+'_'+date+'.mp4')

        try:
	    recipient = video.emailconcursante
	    response = client.send_email(
       		 Destination={
            		'ToAddresses': [
                		recipient,
            		],
        	},
        	Message={
            		'Body': {
          	              'Text': {
                		    'Charset': charset,
                    		    'Data': textbody,
                	       },
            		},
	                'Subject': {
                            'Charset': charset,
                            'Data': subject,
                        },
                },
                Source=sender,
        # Comment or delete the next line if you are not using a configuration set
 #      		 ConfigurationSetName=configSet,
    	   )
        #    server.sendmail("pruebascloud2017@gmail.com", Q.emailconcursante, msg)
        except ClientError as e:
            print(e.response['Error']['Message'])
	else:
            print("Email sent! Message ID:"),
    	    print(response['ResponseMetadata']['RequestId'])


# print(a[0])
