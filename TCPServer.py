from socket import *
import time
import os

#Prepare a sever socket
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverAddress = ('127.0.0.1', serverPort)
serverSocket.bind(serverAddress)
serverSocket.listen(1)

print 'The web server is ready to receive, up on port', serverPort

while True:
	#Establish the connection

	connectionSocket, addr = serverSocket.accept()
	response_header=' '
	print 'Got connection from: ',addr
	message = connectionSocket.recv(1024)
	string = message

	request_method = string.split(' ')[0]
	print 'Test line', request_method
	requestline = string.split('\r\n')[0]
	print 'Status line: ', requestline
	header=string.split('\r\n',1)[1]
	print 'Headers: ',header
	
	if (request_method =='GET'):
		file_requested = string.split(' ')
		file_requested = file_requested[1]
		file_requested = file_requested.split('/')[1]
		print 'Serving web page [',file_requested,']'
		
		try:
			file_handler = open('/Users/johoric/Desktop/web-server/'+file_requested,'rb')
			print '\n\n success \n\n'
			if(request_method == 'GET'):
				response_content = file_handler.read()
			file_handler.close()
			response_header ='HTTP/1.1 200 OK\n'
			current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
			response_header += 'Date: ' + current_date +'\n'
			response_header += 'Server: Lab1TCPServer\n'
			response_header += 'Connection: close\n\n'
			
		except Exception as e:
			print 'Warning, file not found. Serving response code 404\n',e
			response_content = b"<html><body><p>Error 404: File not found</p></body></html>"
			response_header ='HTTP/1.1 404 Not Found\n'
			current_date = time.strftime("%a, %d %b %Y %H:%M:%S",time.localtime())
			response_header += 'Date: ' + current_date +'\n'
			response_header += 'Lab1TCPServer\n'
			response_header += 'Connection: close\n\n'
			
		server_response = response_header.encode()
		
		server_response += response_content
		
		connectionSocket.send(server_response)
		print 'Wait for next process'
		connectionSocket.close()
		import os
os.system("pause")
		
	