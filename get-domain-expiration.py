#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 21:24:54 2020

@author: brianf
"""

import socket

def get_expiration_date(domain):
    domain = domain.replace('http://', '').replace('www.', '')
    registry = get_registry(domain)
    response = query_server(registry, domain)
    expiration = parse_response(response, 'registry expiry date')
    print(expiration)
    return expiration

def get_registry(domain):
    tld = domain.split('.')[-1] # com, org, net ...
    
    # Get the proper registry for the tld from IANA
    response = query_server('whois.iana.org', tld) 
    server = parse_response(response, 'whois')
    return server
    
def query_server(server, query):
    ENCODING = 'utf-8'
    ADDRESS = (server, 43) # whois database uses port 43
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDRESS)
    sock.send((query + '\r\n').encode(ENCODING))
    
    # Recieve response in 4096 byte chunks
    response = ''
    chunk = True
    while chunk:
        chunk = sock.recv(4096).decode(ENCODING)
        response += chunk
        
    sock.close()
    return response
        
def parse_response(text, key):
    'Returns the value for a specific key if found'
    for line in text.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            if k.strip().lower() == key:
                return v.strip().lower()
            
    return 'Key not found'

## Testing
# a = get_expiration_date('sav.com')
# b = get_expiration_date('www.iana.org')
# c = get_expiration_date('usa.gov') # Restricted access
# d = get_expiration_date('authorize.net')