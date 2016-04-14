import json, os
import xml.etree.ElementTree as ET
import re

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    """ from http://stackoverflow.com/questions/4836710/does-python-have-a-built-in-function-for-string-natural-sort"""
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]
            
stateFullNames = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}


inFileName = './govtrackdata/us/113/people.xml'

senateData = {}
states = []

tree = ET.parse(inFileName)
root = tree.getroot()
for child in root:
    if child.tag == 'person':
        for grandchildren in child:
            if grandchildren.attrib['type']=='sen':
                senateData[child.attrib['thomasid']] = {'firstName':child.attrib['firstname'], 'lastName':child.attrib['lastname'], 'party':grandchildren.attrib['party'][0], 'url':grandchildren.attrib['url'], 'state':grandchildren.attrib['state'], 'cosponsoredBills':[]}
                states.append(grandchildren.attrib['state'])
states = set(states)

def get_url_cosponsors(inFileName):
    inFile = open(inFileName, 'r')
    data = json.loads(inFile.read())

    allSponsors = data['cosponsors']
    allSponsors.append(data['sponsor'])

    allSponsorsThomasID = []

    for sponsor in allSponsors:
        if sponsor.has_key('withdrawn_at') == False or sponsor['withdrawn_at'] is None:
            allSponsorsThomasID.append(sponsor['thomas_id'])
    url = data['url']
    return url, allSponsorsThomasID


inDirName = './govtrackdata/congress/113/bills/s/'
senateBillDirs = os.listdir(inDirName)
senateBillDirs.sort(key=natural_sort_key)

billDetails = {}

for senateBillDir in senateBillDirs:
    fullPathThisDir = os.path.join(inDirName, senateBillDir)
    if os.path.isdir(fullPathThisDir):
        inFileNameThisBill = os.path.join(fullPathThisDir, 'data.json')
        urlThisBill, allSponsorsThomasIDs = get_url_cosponsors(inFileNameThisBill)

        billDetails[senateBillDir] = urlThisBill
        for thomasID in senateData.keys():
            if thomasID in allSponsorsThomasIDs:
                senateData[thomasID]['cosponsoredBills'].append("<a href='"+urlThisBill+"'>"+senateBillDir[1:]+"</a>")
                #senateData[thomasID]['cosponsoredBills'].append(senateBillDir)


dataOut = {}
for st in states:
    dataOut[st] = {"description":"<strong>"+stateFullNames[st]+": </strong>"}
    thomasIDsThisState = [tid for tid in senateData.keys() if senateData[tid]['state']==st]
    cosponsoredBillsThisState = 0
    for tid in thomasIDsThisState:
        cosponsoredBillsThisState += len(senateData[tid]['cosponsoredBills'])
        dataOut[st]['description'] = dataOut[st]['description']+"<br /><br /><strong><a href='"+senateData[tid]['url']+"' target='_blank'>"+senateData[tid]['firstName']+' '+senateData[tid]['lastName']+' ('+senateData[tid]['party']+')</a> cosponsored '+str(len(senateData[tid]['cosponsoredBills']))+" Senate bills:</strong> "+' '.join(senateData[tid]['cosponsoredBills'])
        #dataOut[st]['description'] = dataOut[st]['description']+senateData[tid]['firstName']+' '+senateData[tid]['lastName']+' '+str(len(senateData[tid]['cosponsoredBills']))+' '+'; '

    dataOut[st]['fillKey'] = str(int(round((cosponsoredBillsThisState-141)/72.)))

outFileName = 'readData.js'
outFile = open(outFileName, 'w')
outFile.write("var data = ")
json.dump(dataOut, outFile)
outFile.close()
