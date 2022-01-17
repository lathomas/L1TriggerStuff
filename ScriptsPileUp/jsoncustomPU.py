import json

minbiasxs_inpb = 69200.0
min_pu = 50.0
min_instantlumi = min_pu / minbiasxs_inpb
print(min_instantlumi)
result = {}
mylist = list()

#Access the dictionary of good runs/LS. Key is run, value is list of LS
goodrunsandlumisections = {}
with open('Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt', 'r', encoding='utf-8') as f_goodlumi:
    goodrunsandlumisections = json.load(f_goodlumi)

def isgoodrunlumi(run, lumisection):
    '''
    Check the runnb/LS is in the certified JSON
    :param run: run number
    :param lumisection: lumi section
    :return: boolean
    '''
    result = False
    thegoodlumis = goodrunsandlumisections.get(run,[])
    for lumiranges in thegoodlumis:
        if len(lumiranges) == 1:
            if lumisection == lumiranges[0]:
                result = True
        elif lumisection >= lumiranges[0] and lumisection <= lumiranges[1]:
            result = True
    return result


with open('pileup_latest.txt', 'r', encoding='utf-8') as f_in:
    mydata = json.load(f_in)
    '''
    This dictionary has:
    key = run nb 
    value = [[LS1,x,y, <instlumi/bunch>], [LS2,x,y, <instlumi/bunch>],...]
    See: https://twiki.cern.ch/twiki/bin/viewauth/CMS/PileupJSONFileforData#Creating_the_pileup_files
    '''
    for run in mydata:
        mylist = list()
        for lumi in mydata[run]:
            instl = lumi[3]
            #if run=="315322":
            #    print(lumi[0], instl)
            if instl >= min_instantlumi and isgoodrunlumi(run, lumi[0]):
                mylist.append(lumi[0])
        mylist.sort()
        #if len(mylist) > 0:
        #    print(mylist)

        mylistcompressed = list()
        sublist = list()
        for it, val in enumerate(mylist):
            if it == 0:
                sublist.append(val)
            elif val == sublist[-1] + 1 and len(sublist) == 1:
                sublist.append(val)
            elif val == sublist[-1] + 1 and len(sublist) > 1:
                sublist.pop()
                sublist.append(val)
            else:
                mylistcompressed.append(sublist)
                sublist = list()
                sublist.append(val)
        if len(sublist) > 0:
            mylistcompressed.append(sublist)
            sublist = list()

        if len(mylistcompressed) > 0:
            result[run] = mylistcompressed
            #print(mylistcompressed)

with open('highPU_certified.json', 'w', encoding='utf-8') as f_out:
    json.dump(result, f_out, indent=3)