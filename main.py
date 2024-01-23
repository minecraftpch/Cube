import requests
import json

def callScryfall():
    contents = requests.get("https://api.scryfall.com/cards/317f1133-7cf8-4b7a-919e-88c45f8c2c3a").json()
    print(contents)
    print(contents["name"])

# Grabs cardname from scryfall to update the scryfall_id/card_name mapping table
# Parameter: scryfall_id: string -- the scryfall id of the card to be searched
def updateCsv(scryfall_id):
    print('gotta go to the api...')
    contents = requests.get("https://api.scryfall.com/cards/" + scryfall_id).json()
    card_name = contents["name"].replace(',', '*')
    fp = open('id_name_mapping.csv', 'a')
    fp.write(scryfall_id + ',' + card_name + '\n')
    fp.close()
    return card_name

# Gets cardname from csv based on scryfall_id. If the id isn't found, use Scryfall API and save result to csv
# Parameter: scryfall_id: string -- the scryfall id of the card to be searched 
def getCardName(scryfall_id):
    fp = open('id_name_mapping.csv', 'r')
    lines = fp.readlines()
    for line in lines:
        split_line = line.split(',')
        if(split_line[0] == scryfall_id):
            return split_line[1] # card_name
    fp.close()
    return updateCsv(scryfall_id)

# prototype function to demonstrate to Peter looping over the draft log
def getAvgPickForEverything():
    filenames = ['draftLogs/DraftLog_0cc8f92584f9.txt'] # refactor later

    results = {}

    for file in filenames:
        fp = open(file, 'r')
        file_content = json.loads(fp.read())

        users = file_content["users"]

        for username in users:
            user = users[username]
            for pick in user["picks"]:
                #pickNum = (pick["packNum"])*15 + pick["pickNum"]+1
                pickNum = pick["pickNum"]+1
                cardName = getCardName(pick["booster"][pick["pick"][0]])[:-1]
                if cardName in results.keys():
                    results[cardName] += pickNum
                else:
                    results[cardName] = pickNum
        fp.close()
    for cardName in results:
        results[cardName] /= len(filenames)

    keys = []
    for key in results.keys():
        keys.append(key)
    keys.sort(key=lambda card: results[card])

    output = ''
    for key in keys:
        output += key + ' ' + str(results[key]) + '\n'

    return output

# another sample function
def getPack1Pick1Rate():
    filenames = ['draftLogs/DraftLog_0cc8f92584f9.txt'] # refactor later

    results = {}

    for file in filenames:
        fp = open(file, 'r')
        file_content = json.loads(fp.read())

        users = file_content["users"]

        for username in users:
            user = users[username]
            pick1Obj = user["picks"][0]
            for i in range(len(pick1Obj["booster"])):
                cardName = getCardName(pick1Obj["booster"][i])[:-1]
                if i == pick1Obj["pick"][0]:
                    if cardName in results.keys():
                        results[cardName]["picks"] += 1
                    else:
                        results[cardName] = {"picks": 1, "passes": 0}
                else:
                    if cardName in results.keys():
                        results[cardName]["passes"] += 1
                    else:
                        results[cardName] = {"picks": 0, "passes": 1}
        fp.close()
    
    output = ''
    for cardName in results.keys():
        output += cardName + ' ' + str(100 * results[cardName]["picks"] / (results[cardName]["picks"]+results[cardName]["passes"])) + '%\n'
    return output
                    


def main():
    print('Jackson and Peter\'s cube analytics app!')
    #print(getAvgPickForEverything())
    #print(getPack1Pick1Rate())

if __name__ == '__main__':
    main()