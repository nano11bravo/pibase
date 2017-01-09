import urllib
import os 

# Return CPU temperature as a character string                                      
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM                                                                
# Index 1: used RAM                                                                 
# Index 2: free RAM                                                                 
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return information about disk space as a list (unit included)                     
# Index 0: total disk space                                                         
# Index 1: used disk space                                                          
# Index 2: remaining disk space                                                     
# Index 3: percentage of disk used                                                  
def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

# Tries to open the url with the params through the method specified
def fetch_url(url, params, method):
  params = urllib.urlencode(params)
  if method=="GET":
    f = urllib.urlopen(url+"?"+params)
  else:
    # Usually a POST
    f = urllib.urlopen(url, params)
  return (f.read(), f.code)

from uuid import getnode as get_mac
mac = get_mac()

url = "http://sdw.seven-labs.com/pi/"
method = "POST"
params = {"cpu_temp": getCPUtemperature(), "cpu_usage": getCPUuse(), "disk_space": getDiskSpace(), "ram_info": getRAMinfo(), "mac_address": get_mac()}

# Fetch the content and response code
[content, response_code] = fetch_url(url, params, method)

# Check if the server responded with a success code (200)
if (response_code == 200):
  print content
else:
  print content

