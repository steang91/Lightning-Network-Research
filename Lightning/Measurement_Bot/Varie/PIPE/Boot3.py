#lncli -network=testnet queryroutes 03ce542ac3320900154ea33c8dfb0e8faa5e6facd88d5de22b011d135e3f5e906f 500000 --final_cltv_delta=144

#Step 5: Query Routes + Select Route 
while my_string!="UnknownNextPeer":
    cmd3="lncli -network=testnet queryroutes "+choosed_peer+" "+str(capacity_test)+" --final_cltv_delta=144"
    print(cmd3)
    with open('MyRoute.txt', 'w+') as log3:
        c = subprocess.Popen([cmd3], stdout=log3, stderr=log3, shell=True)
        time.sleep(10)
    
    with open('MyRoute.txt','r+') as test_log:
        l=test_log.read()
        if l.startswith("[lncli]"):
            print("Not Possible to measure this channel")
            exit()
			#ACTUALLY HERE IT HAS TO STOP THE EXECUTION AND GO BACK TO 1 Or Going back to channel choice. 
        else:			
            with open('MyRoute.txt') as f:
                data=json.loads(f.read())
                

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
	
#to add an extra hop 
#dataJson['routes'][0]['hops'].append({
#	"chan_id": "1602118184053178368",
#    "chan_capacity": "500000",
#    "amt_to_forward": "90000",
#    "fee": "1",
#    "expiry": 1475903,
#    "amt_to_forward_msat": "90000000",
#    "fee_msat": "1250",
#    "pub_key": "035639efb2bdd73ff6b82374a9d958c7ab404f8c1acb6dee678d9596e7cae25b2c"	
#})



    with open('route.json', 'w') as outfile:  
        json.dump(dataJson,outfile,indent=4)
        time.sleep(10)
	#Timesleephere?
	
    data1=[]

    cmd4='lncli --network=testnet sendtoroute --payment_hash=35ac914ee69d4e30de1a12637fe49d3125ec0560b2b9af5d1b4cdf3884e87512 --routes="$(cat route.json)" -'

    with open('Payment_Attempt.json', 'w+') as log4:
        c = subprocess.Popen([cmd4], stdout=log4, stderr=log4, shell=True)
        time.sleep(10)

    with open('Payment_Attempt.json') as f:
        data=json.loads(f.read())

    k=0
    data1.insert(k,data["payment_error"])

    s = str(data1)
    substring1 = "unable to route payment to destination: " 
    my_string = s[(s.index(substring1)+len(substring1)):(len(s)-2)]
    if my_string=="UnknownNextPeer":
        print(my_string)
    else: 
        substring1 = "ShortChannelID) "
        substring2 = " Timestamp"
        s1=s.index(substring1)+12
        s2=s.index(substring1)
        my_string = s[(s.index(substring1)+len(substring1)):s.index(substring2)]
        my_string=my_string[:-3]
        def_my_string=my_string
        print(my_string)
	capacity_test=(capacity_test)/10
    if capacity_test <10: 
        break	
	
	
	

if def_my_string!="":
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://1ml.com/testnet/")
    assert 'q' in driver.page_source
    action = action_chains.ActionChains(driver)
#action2=action_chains.ActionChains(driver)

# open up the developer console, mine on MAC, yours may be diff key combo


#action.send_keys(keys.Keys.ALT+'1445853:27:0')
#action.perform()
    print("blblblbl")
    print(def_my_string)
#action.perform()
#time.sleep(3) '1480451:9:0'
    action.send_keys(def_my_string)
#action.perform()
    action.send_keys(keys.Keys.ENTER)
    action.perform()

#time.sleep(3)


#to find the exact x path of an element: right click on the element -> analizza elemento -> right click -> copia -> Xpath 
    pageText = driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[1]/ul[2]/li[1]/div/a/h2").text

    print("From the webpage.. here the result: ")
    print(pageText)

    driver.close()


    if os.path.exists("data.json"):
        print("esiste fra")
        with open('data.json') as f:
            data=json.loads(f.read())
    else: 
        print("non esiste fra")
        data = {}  
        data['channels'] = []


  
    data['channels'].append({  
        'Node1_pub_key': address_only_pub,
        'Node2_pub_key': choosed_peer,
        'Channel_ID': pageText,
        'Short_Channel_ID': def_my_string,
        'Capacity': capacity_cp,
        'Real_Capacity': capacity_test, 	
    })
else:
    if os.path.exists("data.json"):
        print("esiste fra")
        with open('data.json') as f:
            data=json.loads(f.read())
    else: 
        print("non esiste fra")
        data = {}  
        data['channels'] = []
		
    data['channels'].append({  
        'Node1_pub_key': address_only_pub,
        'Node2_pub_key': choosed_peer,
        'Channel_ID': channel_temp,
        'Short_Channel_ID': def_my_string,
        'Capacity': capacity_cp,
        'Real_Capacity': capacity_test, 	
    })

#iter(data).next()['edges'] = var


with open('data.json', 'w') as outfile:  
    json.dump(data,outfile,indent=4)
    time.sleep(10)

with open('data.json') as f:
    dataPrint=json.loads(f.read())
	
print(dataPrint)
