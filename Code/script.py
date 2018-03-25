import csv, json, urllib.request, traceback

with open('Cleaned_Data_2.csv', newline='') as f:
    reader = csv.reader(f)
    firstLine = True
    for row in reader:
        if firstLine:
            firstLine = False
            continue
        name = row[1]
        postCodeSto = row[4]
        newName = name.replace(" ", "%20")
        newName += "%20" + postCodeSto
        toURL = "https://maps.googleapis.com/maps/api/geocode/json?address=" + newName + "&key=AIzaSyCqDm-sYF31ZCWizypTghvh2sDqTiFKVYI"
        with urllib.request.urlopen(toURL) as url:
            data = json.loads(url.read().decode())
            try:
                printError = False
                latitude = data["results"][0]["geometry"]["location"]["lat"]
                longitude = data["results"][0]["geometry"]["location"]["lng"]
                toSearch = data["results"][0]["address_components"]
                for a in toSearch:
                    if (a["types"][0] == "postal_code"):
                        postCode = a["long_name"]
                        if(postCode != postCodeSto):
                            printError = True
                #if (postCode != postCodeSto):
                #    print ("ERROR")
                #else:
                if printError:
                    print ("ERROR")
                else:
                    print (latitude, " ", longitude)
            except Exception as e:
                traceback.print_exc()
                print ("ERROR2")
                continue
