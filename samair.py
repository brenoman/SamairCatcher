import unpack
import re
import urllib2
import socket
#testando
import Queue
import threading
import time


MAX_PAGINAS = 30
proxyfile = file("listaproxyes", 'w')



#testando
input_file = 'listaproxyes'
threads = 30

queue = Queue.Queue()
output = []
contadorT=0


def comecaTratamento(threads):
	listaboa = open("listafinal.txt",'w')
	start = time.time()
	#spawn a pool of threads, and pass them queue instance 
	for i in range(threads):
		t = ThreadUrl(queue)
		t.setDaemon(True)
		t.start()
	hosts = [host.strip() for host in open(input_file).readlines()]
	#populate queue with data   
	for host in hosts:
		queue.put(host)
		#wait on the queue until everything has been processed     
	queue.join()

	#pergunta se quer em formato (P)roxychains ou (I)p:port
	print " \n\n Output format? (P)roxychains or (I)p:port?"
	formato = raw_input()
	formato = formato.upper()
	print formato
	if formato != "P" and formato != "I":
		print "Wrong format. Ip:port selected"
		formato = 'I'
	for host in output:
		print "\n\n\n #### FINAL PROXY LIST ###\n\n\n"
		try:
			enderecoip = host[0:host.index(':')]
			portaip = host[host.index(':')+1:]
			print str(enderecoip) + str(portaip) + " ===> " + host
			if formato == 'I':
				listaboa.write(enderecoip +':'+ portaip + '\r\n')
			else:
				listaboa.write("http " + enderecoip +' '+ portaip + '\r\n')
		except Exception,e:
			print e
			continue

	print "Elapsed Time: %s" % (time.time() - start)



class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
	global contadorT
	contador=0
        while True:
            #grabs host from queue
            proxy_info = self.queue.get()
	    contadorT = contadorT + 1
            try:
		print " [" +str(contadorT) + "] Trying " +  proxy_info + " \n"
		
                proxy_handler = urllib2.ProxyHandler({'http':proxy_info})
                opener = urllib2.build_opener(proxy_handler)
                opener.addheaders = [('User-agent','Mozilla/5.0')]
                urllib2.install_opener(opener)
                req = urllib2.Request("http://www.google.com")
                sock=urllib2.urlopen(req, timeout= 7)
                rs = sock.read(1000)
                if '<title>Google</title>' in rs:
		    print "\n\n ### Added: " + proxy_info + "###\n\n"
                    output.append((proxy_info))
                else:
                    raise "Not Google"
            except:
		pass
                #output.append(('x',proxy_info))
            #signals to queue job is done
            self.queue.task_done()

















def intro():
	print '\n\n##################################################################'
	print '################       Samair\'s Proxy Catcher     ################'
	print '##################################################################'
	print '### Version 0.1b'
	print '### Author: desempregad0'
	print '### Github.com/desempregad0'
	print '##################################################################\n\n\n'

	print 'Downloading Samair\'s proxy pages...'

	

	
	
	
	
def getSamairPages():
	global MAX_PAGINAS
	global proxyfile
	i=1
	while i<=MAX_PAGINAS:
		print "["+str(i)+"/30] Downloading Page "+str(i)
		if i < 10:
			resposta = urllib2.urlopen("http://www.samair.ru/proxy/proxy-0"+str(i)+".htm")
		else:
			resposta = urllib2.urlopen("http://www.samair.ru/proxy/proxy-"+str(i)+".htm")
	#	print resposta.read()
		responsa = resposta.read()
		proxies = re.findall(('\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}.*?</'), responsa)
		js = proxies.pop(0)
		js = js[0:js.index(".js")+3]		
		resposta2 = urllib2.urlopen("http://www.samair.ru/js/"+js)	
		traducao = unpack.unpack(resposta2.read())
		traducao = traducao[0:len(traducao)-1]
		#proxyfile.write("trad: "+traducao)
		for aue in proxies:
			try:	
				dicionariotraducao = dict(item.split("=") for item in traducao.split(";"))
				ip = aue[0:aue.index('<')]
				porta = aue[aue.index('":"')+4:]
				porta = porta[0:len(porta)-3]			
				pattern = re.compile(r'\b(' + '|'.join(dicionariotraducao.keys()) + r')\b')
				result = pattern.sub(lambda x: dicionariotraducao[x.group()], porta)
				ipporta = ip + ":" +str(result).replace("+","")
				proxyfile.write(ipporta+"\n")
			except Exception, e:
				#print e
				continue
		i+=1
	proxyfile.close()
	print str(i-1)+" Pages downloaded. How many threads to see which is working?"


def main():
	intro()
	getSamairPages()
	print "How many threads to see which is working?"
	numeroThreads = int(raw_input())
	comecaTratamento(numeroThreads)
	
main()