import json 
import subprocess
import time 
import os 
from random import randint
import pandas as pd
#Global Variable: 
res=-1
address_only_pub=""
address=""
p=0
choosed_peer=""
capacity_cp=0
channel_temp=""
my_string=""
def_my_string=""
capacity_test=0
my_string=""
def_my_string=""
num_chan=0 
channel_direction=2
TxID=""
ConnectO=""
route={}
payment_hashList = ['3','5','a','b','9','1','4','e','3','b','9','d','4','e','3','0','d','e','1','a','1','2','6','3','7','f','e','4','9','d','3','1','2','5','e','c','0','5','6','0','b','2','b','9','a','f','5','d','1','b','4','c','d','f','3','8','8','4','e','8','7','5','1','2']
payment_hash= ''.join(payment_hashList)
channel_direction=0
#oldtestnode:0260d9119979caedc570ada883ff614c6efb93f7f7382e25d73ecbeba0b62df2d7@88.99.209.230:9735
#newtestnode: 

def Connection_To_Peer(ad,ad_ip):
#Step 1: Connection to target peer
    global p 
    global address_only_pub
    global address
    global ConnectO	
    p=0
    address_only_pub=ad
    address=ad_ip
   
    
def Channel_Establishment():
    #Step 2: Channel Creation 
    #value=4200000
    global TxID
    global p 
    global address_only_pub
    global address 
    value=4500000 
    #value=20000		   
    cmd2="lncli -network=testnet openchannel "+address_only_pub+" "+str(value)
    now2 = subprocess.Popen([cmd2],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    output,error=now2.communicate()
    if(output==""):
        now2=error
    else:
        now2=output
				
    if now2.startswith("[lncli]"):
        print("Channel Establishment failed:")
        return(0)
    elif now2.startswith("{"):
        print("Channel Created!")	
        creation=json.loads(now2)
        TxID=creation["funding_txid"]
        print("The Funding Transaction is: "+str(TxID))
        cmd2_1="lncli -network=testnet listchannels"    
        log2_1= subprocess.Popen([cmd2_1],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        output,error=log2_1.communicate()
        list=output
        ok=0
        while(ok!=1):
            cmd2_1="lncli -network=testnet listchannels"
            log2_1= subprocess.Popen([cmd2_1],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            output,error=log2_1.communicate()
            list=json.loads(output)
            j=0
            for i in list["channels"]:
                ap=list["channels"][j]["channel_point"]
                ap=ap[0:64]
                print(ap,TxID)
                j=j+1
                if(ap==TxID):
                    ok=1
            if(ok==1):
                print("Channel with reference "+str(TxID)+" has been included in the blockchain")
            else:
                print("We have to wait 4 minutes to check again the channel opening")
                time.sleep(240)			
    return(1)

def Close_Channel():
    global p 
    global address_only_pub
    global address	
    global TxID		   
    cmd2="lncli -network=testnet closeallchannels"
    c = subprocess.Popen([cmd2],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    print("Channel closing Try")
    c.communicate()
    cmdc="lncli -network=testnet pendingchannels"
    c2 = subprocess.Popen([cmdc],stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)	
    output,error=c2.communicate()
    closing=json.loads(output)        
    ok=0
    while(ok!=1):
        c2 = subprocess.Popen([cmdc],stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)	
        output,error=c2.communicate()
        closing=json.loads(output)        
        if(len(closing["waiting_close_channels"])!=0 or len(closing["pending_closing_channels"])!=0): 
            print(closing["waiting_close_channels"],closing["pending_closing_channels"])
            print("We have to wait 4 minutes to check again the channel closing")
            time.sleep(240)
        else:
            print(closing["waiting_close_channels"],closing["pending_closing_channels"])
            print("Channel to peer "+str(address_only_pub)+"successfully closed")			
            ok=1
    return(1)		


	

def Choose_Channel():
    global p 
    global address_only_pub
    global address 
    global choosed_peer
    global capacity_cp
    global channel_temp
    global capacity_test
    global my_string
    global def_my_string
    global num_chan
    global channel_direction
    
    
	
def Query_Select_Routes(LambdaT):
    global address_only_pub
    global choosed_peer
    global capacity_test
    global my_string
    global def_my_string
    testFail=0
    cmd3="lncli -network=testnet queryroutes "+choosed_peer+" "+str(LambdaT)+" --final_cltv_delta=144"
    log3 = subprocess.Popen([cmd3], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output,error=log3.communicate()
    if(error!="" or output==""):
        testFail=1
        print("Capacity Test failed")
        return (testFail)
    else:			
        data=json.loads(output)            
    dataJson={}

    dataJson['routes'] = []
    dataPrint=[]

#first hop : 0269a94e8b32c005e4336bfb743c08a6e9beb13d940d57c479d95c8e687ccbdb9f Previous: 038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9
#second hoP: 03ecd95e86e780ae82139c3217b527073622d28c4d8a53b76142a7b7b1d1e36975  Previous: 02fd753c8ad77d2601637b6add4362fec59f4d3e8190347ab4d155f3e9a76e113c
	
    k=0 
    j=0
    for i in data["routes"]:
        if data["routes"][k]["hops"][0]["pub_key"]==address_only_pub or data["routes"][k]["hops"][0]["pub_key"]==choosed_peer:
            if data["routes"][k]["hops"][1]["pub_key"]==address_only_pub or data["routes"][k]["hops"][1]["pub_key"]==choosed_peer:
                dataJson['routes'].append({  
                'total_time_lock': data['routes'][k]['total_time_lock'],
                'total_fees': data['routes'][k]['total_fees'],
                'total_amt': data['routes'][k]['total_amt'],
                })
                dataJson['routes'][0]['hops']=[]
                dataJson['routes'][0]['hops'].append({
	            "chan_id": data["routes"][k]["hops"][0]['chan_id'],
                "chan_capacity": data["routes"][k]["hops"][0]['chan_capacity'],
                "amt_to_forward": data["routes"][k]["hops"][0]['amt_to_forward'],
                "fee": data["routes"][k]["hops"][0]['fee'],
                "expiry": data["routes"][k]["hops"][0]['expiry'],
                "amt_to_forward_msat": data["routes"][k]["hops"][0]['amt_to_forward_msat'],
                "fee_msat": data["routes"][k]["hops"][0]['fee_msat'],
                "pub_key": data["routes"][k]["hops"][0]['pub_key'] 	
                })
                dataJson['routes'][0]['hops'].append({
	            "chan_id": data["routes"][k]["hops"][1]['chan_id'],
                "chan_capacity": data["routes"][k]["hops"][1]['chan_capacity'],
                "amt_to_forward": data["routes"][k]["hops"][1]['amt_to_forward'],
                "fee": data["routes"][k]["hops"][1]['fee'],
                "expiry": data["routes"][k]["hops"][1]['expiry'],
                "amt_to_forward_msat": data["routes"][k]["hops"][1]['amt_to_forward_msat'],
                "fee_msat": data["routes"][k]["hops"][1]['fee_msat'],
                "pub_key": data["routes"][k]["hops"][1]['pub_key'] 	
                })  
                dataJson['routes'][0]['hops'].append({
                "chan_id": "1602118184053178368",
                "chan_capacity": "500000",
                "amt_to_forward": "90000",
                "fee": "1",
                "expiry": 1475903,
                "amt_to_forward_msat": "90000000",
                "fee_msat": "1250",
                "pub_key": "035639efb2bdd73ff6b82374a9d958c7ab404f8c1acb6dee678d9596e7cae25b2c"	
                })
                dataJson['routes'][0]["total_fees_msat"]=data["routes"][k]["total_fees_msat"] 
                dataJson['routes'][0]["total_amt_msat"]=data["routes"][k]["total_amt_msat"] 
                break
        
        k=k+1
    with open('route.json', 'w') as outfile:  
        json.dump(dataJson,outfile,indent=4)
    return(0)
	
	                                                                                                    
# lncli queryroutes 03e567bce8a40f5c36f6d431102290ad82cd99f9abca6b3f11aabcdd46f1d7bfcc 3999001 --final_cltv_delta=144
def EnoughCapacity(LambdaT):
#lncli queryroutes 03ce542ac3320900154ea33c8dfb0e8faa5e6facd88d5de22b011d135e3f5e906f 500000 --final_cltv_delta=144
#Step 5: Query Routes + Select Route 
        #time.sleep(10) what happen here if I delete the sleep? 
    global address_only_pub
    global choosed_peer
    global capacity_test
    global my_string
    global def_my_string
    global payment_hash
    global payment_hashList
    start=time.time()
    dataJson={}
    dataJson['routes'] = []
    dataPrint=[]
    with open('route.json','r+')as rt:
        data=json.loads(rt.read())
#first hop : 0269a94e8b32c005e4336bfb743c08a6e9beb13d940d57c479d95c8e687ccbdb9f Previous: 038863cf8ab91046230f561cd5b386cbff8309fa02e3f0c3ed161a3aeb64a643b9
#second hoP: 03ecd95e86e780ae82139c3217b527073622d28c4d8a53b76142a7b7b1d1e36975  Previous: 02fd753c8ad77d2601637b6add4362fec59f4d3e8190347ab4d155f3e9a76e113c
	
    dataJson['routes'].append({  
    'total_time_lock': data['routes'][0]['total_time_lock'],
    'total_fees': data['routes'][0]['total_fees'],
    'total_amt': str(int(LambdaT)+int(data['routes'][0]['total_fees'])),
    })
    dataJson['routes'][0]['hops']=[]
    dataJson['routes'][0]['hops'].append({
	"chan_id": data["routes"][0]["hops"][0]['chan_id'],
    "chan_capacity": data["routes"][0]["hops"][0]['chan_capacity'],
    "amt_to_forward": str(LambdaT),
    "fee": data["routes"][0]["hops"][0]['fee'],
    "expiry": data["routes"][0]["hops"][0]['expiry'],
    "amt_to_forward_msat": str(int(LambdaT)*1000), 
    "fee_msat": data["routes"][0]["hops"][0]['fee_msat'],
    "pub_key": data["routes"][0]["hops"][0]['pub_key'] 	
    })
    dataJson['routes'][0]['hops'].append({
	"chan_id": data["routes"][0]["hops"][1]['chan_id'],
    "chan_capacity": data["routes"][0]["hops"][1]['chan_capacity'],
    "amt_to_forward": str(LambdaT),
    "fee": data["routes"][0]["hops"][1]['fee'],
    "expiry": data["routes"][0]["hops"][1]['expiry'],
    "amt_to_forward_msat": str(int(LambdaT)*1000),
    "fee_msat": data["routes"][0]["hops"][1]['fee_msat'],
    "pub_key": data["routes"][0]["hops"][1]['pub_key'] 	
    })  
    dataJson['routes'][0]['hops'].append({
    "chan_id": "1602118184053178368",
    "chan_capacity": "500000",
    "amt_to_forward": "90000",
    "fee": "1",
    "expiry": 1475903,
    "amt_to_forward_msat": "90000000",
    "fee_msat": "1250",
    "pub_key": "035639efb2bdd73ff6b82374a9d958c7ab404f8c1acb6dee678d9596e7cae25b2c"	
    })
    dataJson['routes'][0]["total_fees_msat"]=data["routes"][0]["total_fees_msat"] 
    dataJson['routes'][0]["total_amt_msat"]=str(int(LambdaT)*1000+int(data["routes"][0]["total_fees_msat"])) 
        
    with open('route1.json', 'w+') as outfile:  
        json.dump(dataJson,outfile,indent=4)		 
    data1=[]

    cmd4='lncli sendtoroute '+str(payment_hash)+' --routes="$(cat route1.json)" -'
    c = subprocess.Popen([cmd4], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    
    output1,error1=c.communicate()
    data=json.loads(output1)
    k=0
    data1.insert(k,data["payment_error"])
    print(cmd4)
    s = str(data1)
    if(s=="[u'payment is in transition']" or s=="[u'payment attempt not completed before timeout of 1m0s']" or s=="[u'unable to route payment to destination: TemporaryNodeFailure']"):
        print(s)
        rand=randint(0,9)
        rand2=randint(4,63)
        print(payment_hash)
        payment_hashList[rand2]=str(rand)
        payment_hash= ''.join(payment_hashList)
        print(payment_hash)
        return(2)
    else:
        substring1 = "unable to route payment to destination: " 
        my_string = s[(s.index(substring1)+len(substring1)):(len(s)-2)]
        if my_string=="UnknownNextPeer":
            testFail=0
            print(my_string)
            end=time.time()
            print("Partial Measurement Time: "+str(end-start))
            return (testFail)
        else: 
            substring1 = "ShortChannelID) "
            substring2 = " Timestamp"
            s1=s.index(substring1)+12
            s2=s.index(substring1)
            my_string = s[(s.index(substring1)+len(substring1)):s.index(substring2)]
            my_string=my_string[:-3]
            def_my_string=my_string
            testFail=1
            print(my_string)
            end=time.time()
            print("Partial Measurement Time: "+str(end-start))
            return (testFail)

def EstimateCapacity():
    start1=time.time()
    global capacity_test
    global channel_direction
    error=0
    epsilon2= 10
    reductionFactor=2
    IterationNum=6
    L=capacity_test
    epsilon=1000
    Lt=0
    Lmax=0
    Lmin=0
    if(Query_Select_Routes(L)==1):
        if(Query_Select_Routes(epsilon)==1):
            return(-1,0)
        else:
            Lt=L/reductionFactor
            Lmax=L
            Lmin=0
            counter=0
            while(counter<IterationNum):
                r1=EnoughCapacity(Lt)
                if(r1==2):
                    return(-2,0)
                if(r1==0):
                    Lmin=Lt
                    Lt=(Lmax+Lmin)/2
                else:
                    Lmax=Lt
                    if(Lmin==0):
                        Lt=Lt/reductionFactor
                    else:
                        Lt=(Lmax+Lmin)/2
                counter=counter+1
            mean=(Lmax+Lmin)/2
            print(mean)
            end1=time.time()
            print("Tempo di esecuzione per la misura di un canale: "+str(end1-start1))
            if(channel_direction==0):
                return(L-mean,(end1-start1))
            else:
                return(mean,(end1-start1))
    else:
        r1=EnoughCapacity(L)
        if(r1==2):
            return(-2,0)
        if(r1==0):
            end1=time.time()
            print("Tempo di esecuzione per la misura di un canale: "+str(end1-start1))
            if(channel_direction==0):            
                return(0,(end1-start1))
            else:
                return(L,(end1-start1))
        Lt=L/reductionFactor
        Lmax=L
        Lmin=0
        counter=0
        while(counter<IterationNum):
            r1=EnoughCapacity(Lt)
            if(r1==2):
                return(-2,0)
            if(r1==0):
                Lmin=Lt
                Lt=(Lmax+Lmin)/2
            else:
                Lmax=Lt
                if(Lmin==0):
                    Lt=Lt/reductionFactor
                else:
                    Lt=(Lmax+Lmin)/2
            counter=counter+1
        mean=(Lmax+Lmin)/2
        print(mean)
        end1=time.time()
        print("Tempo di esecuzione per la misura di un canale: "+str(end1-start1))
        if(channel_direction==0):
            return(L-mean,(end1-start1))
        else:
            return(mean,(end1-start1))		
    	
def Check_Channel(estimation,mtime):
    global def_my_string
    global channel_direction
    if def_my_string!="":

        if os.path.exists("data.json"):
            print("Opening Existing Data File")
            with open('data.json') as f:
                data=json.loads(f.read())
        else: 
            print("Creating Data File")
            data = {}  
            data['channels'] = []


        data['channels'].append({  
            'Node1_pub_key': address_only_pub,
            'Node2_pub_key': choosed_peer,
            'Channel_ID': channel_temp,
            'Capacity': capacity_cp,
            'EstimatedCapacity': estimation,
            'ShortChannelID': def_my_string,
            'Channel_direction': channel_direction,
            'MeasurementTime': mtime,			
        })
    else:
        if os.path.exists("data.json"):
            print("Opening Existing Data File")
            with open('data.json') as f:
                data=json.loads(f.read())
        else: 
            print("Creating Data File")
            data = {}  
            data['channels'] = []
		
        data['channels'].append({  
            'Node1_pub_key': address_only_pub,
            'Node2_pub_key': choosed_peer,
            'Channel_ID': channel_temp,
            'Capacity': capacity_cp,
            'EstimatedCapacity': estimation,
            'ShortChannelID': def_my_string,
            'Channel_direction': channel_direction,
            'MeasurementTime': mtime,			
        })

#iter(data).next()['edges'] = var
    with open('data.json', 'w') as outfile:  
        json.dump(data,outfile,indent=4)
        #time.sleep(10)


	
def Measurement():
    global res
    global address_only_pub
    global address
    global p
    global choosed_peer
    global capacity_cp
    global channel_temp
    global my_string
    global def_my_string
    global capacity_test
    global my_string
    global def_my_string
    global num_chan
    global channel_direction
    
    Retrieve_Channel()
    print(p,num_chan)
    while (p<1):
        Choose_Channel()
        meann,tx= EstimateCapacity()
        print("IL RISULTATO DEL TEST E':")
        print(meann,tx)
        Check_Channel(meann,tx)
        print("Channel Under Test is the number "+str(p)) 
        print(str(num_chan-p)+" still to Test")
        def_my_string=""
        print(num_chan,p)
        break
    
    #Close_Channel()
    return(1)
   
def Main():
    global res
    global address_only_pub
    global address
    global p
    global choosed_peer
    global capacity_cp
    global channel_temp
    global my_string
    global def_my_string
    global capacity_test
    global my_string
    global def_my_string
    global num_chan
    global channel_direction
    start=time.time()    
    address_only_pub="03538c45e97be30bf01623fdec4b27355beef75ab797d3ada61091807febaeede9"
    address="03538c45e97be30bf01623fdec4b27355beef75ab797d3ada61091807febaeede9@163.117.166.53:9935"
	cmd="lncli -network=testnet connect "+address
    print(payment_hash)
    cmd_net="lncli -network=testnet describegraph >mainnet_graph.json"
    c = subprocess.Popen([cmd_net],shell=True)
    c.communicate()
    log=subprocess.Popen([cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True) 
    log2,log3=log.communicate()
    if(log2==""):
        ConnectO=str(log3)
    else:
        ConnectO=str(log2)
    
    now=ConnectO
    if now.startswith("[lncli] rpc error: code = Unknown desc = already connected to peer: "):
        print("Peer Arleady Connected")
    else:
        if now.startswith("[lncli]"): 
            print("Connection Error:")
        elif now.startswith("{"):
            print("Connection Established with peer :"+address)
    
	
    
    j=0
    with open('mainnet_graph.json') as f:
    data=json.loads(f.read())
    dataJson={}
    dataJson['channels'] = []
    k=0
    for i in data["edges"]:
        if data["edges"][k]["node1_pub"]==address_only_pub:
            if data["edges"][k]["node1_policy"]!=None:
                if data["edges"][k]["node2_policy"]!=None:
                    dataJson['channels'].append({  
                    'node1_pub': data["edges"][k]["node1_pub"],
                    'node2_pub': data["edges"][k]["node2_pub"],
                    'channel_id': data["edges"][k]["channel_id"],
                    'capacity': data["edges"][k]["capacity"],
                    'real_capacity':-1,
                    'channel_direction':1
                    })
        else:
            if data["edges"][k]["node2_pub"]==address_only_pub:
                if data["edges"][k]["node1_policy"]!=None:
                    if data["edges"][k]["node2_policy"]!=None:
                        dataJson['channels'].append({  
                        'node2_pub': data["edges"][k]["node1_pub"],
                        'node1_pub': data["edges"][k]["node2_pub"],
                        'channel_id': data["edges"][k]["channel_id"],
                        'capacity': data["edges"][k]["capacity"],
                        'real_capacity':-1,
                        'channel_direction':0
                        })
        
        k=k+1
    with open('data_test.json', 'w') as outfile:  
        json.dump(dataJson,outfile,indent=4)
    with open('data_test.json') as f:
        Channel_Data=json.loads(f.read())
    num_chan=(len(Channel_Data['channels']))
    print(p,num_chan)
    while (p<num_chan):
    
	with open('data_test.json') as f:
        Channel_Data=json.loads(f.read())
    
    if p==num_chan:
        print("All channel have been tested")  #shall we put this in a variable and analize this variable before proceding to query route steps.
    else:
        for i in range(p,num_chan):
            print(i)
            if 	Channel_Data["channels"][p]["real_capacity"]==-1:
                if int(Channel_Data["channels"][p]["capacity"])>=4294967:	
                    print("Channel has a capacity too High")
                    Channel_Data["channels"][p]["real_capacity"]=-2
                else:
                    capacity_cp= int(Channel_Data["channels"][p]["capacity"])
                    choosed_peer=Channel_Data["channels"][p]["node2_pub"]
                    channel_temp=Channel_Data["channels"][p]["channel_id"]
                    channel_direction=Channel_Data["channels"][p]["channel_direction"]
                    p=p+1
                    break
            p=p+1
        with open('data_test.json', 'w') as outfile:  
            json.dump(Channel_Data,outfile,indent=4)	
    print(p)
    print (capacity_cp)
    print(choosed_peer)
    capacity_test=capacity_cp
	
	
    meann,tx= EstimateCapacity()
    print("IL RISULTATO DEL TEST E':")
    print(meann,tx)
    Check_Channel(meann,tx)
    print("Channel Under Test is the number "+str(p)) 
    print(str(num_chan-p)+" still to Test")
    def_my_string=""
    print(p,num_chan)
		
    if(m==1):
        end=time.time()
        print("Peer "+str(peerList[0][i])+" Measurement successfully ended in :"+str(end-start)+" seconds!!")
        m=0
	
		

    