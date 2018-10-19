import sys
import re
import socket
import requests
import json
import pprint
from ipwhois import IPWhois
from urllib2 import urlopen

ip = raw_input('Enter IP address:\n')

try:
	socket.inet_aton(ip)

except socket.error:
	print "IP address is invalid."
	sys.exit()    

def ipinfo():
		
		url = 'http://ipinfo.io/' + ip + '/json'
		print "Getting information from ipinfo.com:\n"
    		result = requests.head(url)	

		if result.status_code == 429:
			print "Unable to fetch data. Switching to Ipapi.com:"
			ipapi()
			sys.exit()	
		output(url)
		return url
	
def ipapi():
		url = 'http://ipapi.co/' + ip + '/json'
		result = requests.head(url)	

		if result.status_code == 429:
			print "Unable to fetch data. Switching to Ipdata.com:"
			ipdata()
			sys.exit()
		output(url)			
		return url
		
def ipdata():
		
		url = 'https://api.ipdata.co/' + ip
		result = requests.head(url)	
		
		if result.status_code == 403:
			print "Unable to fetch data. Switching to extreme-ip-lookup.com:"
			extremeiplookup()
			sys.exit()
		output(url)
		return url
		
def extremeiplookup():
		
		url = 'https://extreme-ip-lookup.com/json/' + ip
    		result = requests.head(url)	

		if result.status_code != 200:
			print "Unable to fetch data. Switching to whois.com:"
			whois()
			sys.exit()
		
		output(url)
		return url		
		
def whois():

		obj = IPWhois(ip)
		results = obj.lookup_rws()
		pprint.pprint(results)
		sys.exit()

def output(url1):

		response = urlopen(url1)
		datafound = json.load(response)

		try:
			city = datafound['city']
			region = datafound['region']
	
			if 'query' in datafound:
				IP = datafound['query']
			elif 'ip' in datafound: 
				IP = datafound['ip']
			if 'organisation' in datafound: 
				organisation = datafound['organisation']
			elif 'org' in datafound:
				organisation = datafound['org']
			if 'country_name' in datafound: 
				country = datafound['country_name']
			elif 'country' in datafound:
				country = datafound['country']
			if 'asn' in datafound:
				asn = datafound['asn']
				print '\nInformation Found: \nIP: {0} \nRegion: {1} \nCountry: {2} \nCity: {3} \nOrg: {4} \nASN: {5}'.format(IP,region,country,city,organisation,asn)
			else:
				print '\nInformation Found: \nIP: {0} \nRegion: {1} \nCountry: {2} \nCity: {3} \nOrg: {4}'.format(IP,region,country,city,organisation)
		except:
			print "Key Error"

if __name__ == "__main__":
    ipinfo()
