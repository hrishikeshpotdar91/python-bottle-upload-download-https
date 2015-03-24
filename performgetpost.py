#UTA ID - 1001048659
#Hrishikesh Potdar 

#References - Bottle API for python
#References - How to upload files bottle http://stackoverflow.com/questions/14296438/bottle-file-upload-and-process 
# Multithreading in bottle  http://stackoverflow.com/questions/19604648/threading-a-bottle-app

from bottle import route, run, get, post, request, response
import threading
import requests
import socket
import os

#Connecting with Socket

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();
 
print 'Our socket has been created'
host = 'localhost'
port = 8080
remote_ip = socket.gethostbyname( host )

print 'Ip address of' + host + ' is ' + remote_ip + 'and we are connected!'

# Uploading file on the server from client side and updating log with file details and http response
@get('/upload')
def upload_view():
	return """
<form action="/upload" method="post" enctype="multipart/form-data">
<input type="text" name="name" />
<input type="file" name="data" />
<input type="submit" name="submit" value="upload now" />
</form>
"""
 
@post('/upload')
def do_upload():
 name = request.forms.get('name') # passing variable from form 
 data = request.files.get('data') #passing variable from form
 response.status = 404

 if name is not None and data is not None:
    response.status = 200
    raw = data.file.read() 
    name, ext = os.path.splitext(data.filename)
    filen = data.filename 
     

    with open(name,'w') as open_file: #uploading file to the server 
     open_file.write(raw)

    logstatus = open("log.txt",'a') #writing details in log file 
    logstatus.write("POST - "+str(os.stat("/home/hduser/Downloads/"+data.filename)))
    logstatus.write("POST - "+str(response.status)+"\n\n\t")  
     
    return "Hello %s! You uploaded %s (%d bytes)." % (name, filen, len(raw))
       	 

  
        
 return "You missed a field."

#Getting a file from the server and saving it locally and updating the log with appropriate http status code  

@get('/download')
def download():
    return '''
        <form action="/download" method="post">
  Select a file: <input type="text" name="upload" />
  <input type="submit" value="download" />
  </form>
    '''
 
@post('/download')
def do_download():
    
    upload   = request.forms.get('upload') #getting input from form 
    
    if os.path.exists(os.getcwd()+"/"+upload): #checking if the path exists
        currentfile = open(os.getcwd()+"/"+upload,'r')
        directory = "/home/hduser/Downloads"
        newvar = open(directory+"/"+upload,'w')
        newvar.write(currentfile.read())
        so = str(currentfile.read())
        hello = "user"
        with open("log.txt",'a') as fo:  # writing details in log file
         fo.write("GET - "+str(response.status)+"\t \t \n")
         fo.write(str(os.stat(os.path.basename(os.getcwd()+"/"+upload)))+"\t\t\n")
         fo.write("File stored at - "+directory+"/"+upload)
         
        so = currentfile.read() 
        return "Hello %s! content of file %s has been downloaded to /home/hduser/downloads" % (hello,so) 
   
      
    if not os.path.exists(os.getcwd()+"/"+upload): # if the path doesn't exist 
       with open("log.txt",'a') as ko:
        ko.write("404 NOT_FOUND \t \t \n")
       return "HTTP 404 file not found"

    

#Multithreading part 

threading.Thread(target=run, kwargs=dict(host='localhost', port=8080)).start()
