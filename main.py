from json import dumps as jsonDumps, loads as jsonLoads
from websocket import create_connection
from random import randint, choices
from pystyle import Write, Colors
from threading import Thread
from time import time, sleep
from requests import get
from uuid import uuid4
from os import system

import solve_challange

clear = lambda: system('cls')
system('title K BOTTER - www.kolmicodes.xyz')

playerCount = 0
failCount = 0
exitVal = False

bypassCharacters = {'a': 'ᗩ', 'b': 'ᗷ', 'c': 'ᑕ', 'd': 'ᗪ', 'e': 'E', 'f': 'ᖴ', 'g': 'G', 'h': 'ᕼ', 'i': 'I', 'j': 'ᒍ', 'k': 'K', 'l': 'ᒪ', 'm': 'ᗰ', 'n': 'ᑎ', 'o': 'O', 'p': 'ᑭ', 'q': 'ᑫ', 'r': 'ᖇ', 's': 'ᔕ', 't': 'T', 'u': 'ᑌ', 'v': 'ᐯ', 'w': 'ᗯ', 'x': '᙭', 'y': 'Y', 'z': 'ᘔ'}
chars = ''

for char in bypassCharacters:
    chars = chars + bypassCharacters[char]

def printLogo():
    Write.Print(f"""
\tdb   dD      d8888b.  .d88b.  d888888b d888888b d88888b d8888b.
\t88 ,8P'      88  `8D .8P  Y8. `~~88~~' `~~88~~' 88'     88  `8D
\t88,8P        88oooY' 88    88    88       88    88ooooo 88oobY'    K Botter
\t88`8b        88~~~b. 88    88    88       88    88~~~~~ 88`8b      www.kolmicodes.xyz
\t88 `88.      88   8D `8b  d8'    88       88    88.     88 `88.
\tYP   YD      Y8888P'  `Y88P'     YP       YP    Y88888P 88   YD
════════════════════════════════════════════════════════════════════════════════════════════════════════════════  
""", Colors.red_to_blue, interval=0)
    
def bypassName(playerName):
    bypassedName = ""
    try:
        playerName = playerName.lower()
    
        for character in playerName:
            try:
                bypassedName = bypassedName + bypassCharacters[character]
            except:
                bypassedName = bypassedName + character  
    except:
        return ''.join(choices(chars, k=5))
    
    return bypassedName

def join_game(gamePin, playerName):
    global playerCount
    global failCount

    try:
        l_data = randint(100, 999)
        o_data = randint(-999, -100)

        generated_uuid = str(uuid4())
        cookies = {
            'generated_uuid': generated_uuid,
            'player': 'active',
        }

        response = get(f'https://kahoot.it/reserve/session/{gamePin}/?{time()}', cookies=cookies )
        session_token = response.headers["X-Kahoot-Session-Token"]
        challange_text = response.json()["challenge"]
        wss_connection = solve_challange.solveChallenge(challange_text, session_token)

        ws = create_connection(f"wss://kahoot.it/cometd/{gamePin}/{wss_connection}")
        ws.send(jsonDumps([{"id":"1","version":"1.0","minimumVersion":"1.0","channel":"/meta/handshake","supportedConnectionTypes":["websocket","long-polling","callback-polling"],"advice":{"timeout":60000,"interval":0},"ext":{"ack":True,"timesync":{"tc":str(time()),"l":0,"o":0}}}]))

        clientId = jsonLoads(ws.recv())[0]["clientId"]

        ws.send(jsonDumps([{"id":"2","channel":"/meta/connect","connectionType":"websocket","advice":{"timeout":0},"clientId":clientId,"ext":{"ack":0,"timesync":{"tc":str(time()),"l":l_data,"o":o_data}}}]))
        ws.recv()

        ws.send(jsonDumps([{"id":"3","channel":"/meta/connect","connectionType":"websocket","clientId":clientId,"ext":{"ack":1,"timesync":{"tc":str(time()),"l":l_data,"o":o_data}}}]))

        while True:
            x = jsonDumps([{"id":"4","channel":"/service/controller","data":{"type":"login","gameid":gamePin,"host":"kahoot.it","name":playerName,"content":"{\"device\":{\"userAgent\":\"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\",\"screen\":{\"width\":920,\"height\":974}}}"},"clientId":clientId,"ext":{}}])

            ws.send(x)
            findit = ws.recv()

            if '"loginResponse","cid":' in findit:
                print(f'{Colors.green} [+] Bot {playerCount} added.')
                playerCount += 1
                break
            
        ws.send(jsonDumps([{"id":"5","channel":"/service/controller","data":{"id":16,"type":"message","gameid":gamePin,"host":"kahoot.it","content":"{\"usingNamerator\":false}"},"clientId":clientId,"ext":{}}]))
        ws.send(jsonDumps([{"id":"6","channel":"/meta/connect","connectionType":"websocket","clientId":clientId,"ext":{"ack":2,"timesync":{"tc":str(time()),"l":l_data,"o":o_data}}}]))

        a = 2
        b = 6
        while True:
            a += 1
            b += 1
            ws.send(jsonDumps([{"id":b,"channel":"/meta/connect","connectionType":"websocket","clientId":clientId,"ext":{"ack":a,"timesync":{"tc":str(time()),"l":l_data,"o":o_data}}}]))
            ws.recv()
    except KeyboardInterrupt:
        pass
    except:
        print(f'{Colors.red} [-] Failed to add bot {playerCount}.')
        playerCount += 1
        failCount += 1
        pass

def main():
    global exitVal

    if exitVal:
        exit(1)

    global playerCount
    global failCount
    currentPlayerCount = 0
    
    try:
        clear()
        printLogo()
        Write.Print(f'┌──<Enter Game Pin>─[~]', Colors.red_to_blue, interval=0.0000)
        Write.Print(f'\n└──╼ $ ', Colors.red_to_blue, interval=0.0000)
        gamePin = input(f'{Colors.purple}').strip()

        clear()
        printLogo()
        Write.Print(f'┌──<Enter Player Name>─[~]', Colors.red_to_blue, interval=0.0000)
        Write.Print(f'\n└──╼ $ ', Colors.red_to_blue, interval=0.0000)
        playerName = input(f'{Colors.purple}').strip()

        clear()
        printLogo()
        Write.Print(f'┌──<Enter Player Amount>─[~]', Colors.red_to_blue, interval=0.0000)
        Write.Print(f'\n└──╼ $ ', Colors.red_to_blue, interval=0.0000)
        playerAmount = input(f'{Colors.purple}')

        clear()
        printLogo()
        Write.Print(f'┌──<Use name bypass [y/n]>─[~]', Colors.red_to_blue, interval=0.0000)
        Write.Print(f'\n└──╼ $ ', Colors.red_to_blue, interval=0.0000)
        nameBypass = input(f'{Colors.purple}')

        if 'y' in nameBypass.lower():
            playerName = bypassName(playerName)

        clear()
        printLogo()

        for i in range(int(playerAmount)):
            currentPlayerCount += 1

            t = Thread(target=join_game,args=[gamePin, f"{playerName}{currentPlayerCount}"]).start()
            sleep(0.01)
    
        while True:
            if playerCount == int(playerAmount):
                break

        clear()
        printLogo()
        
        exitVal = True
        if playerCount - failCount != 0:
            Write.Print(f'[#] Succesfully added {playerCount - failCount} of {playerCount} bots.\n', Colors.green, interval=0.0000)
        else:
            Write.Print(f'\n[#] Failed to add bots.\n', Colors.red, interval=0.0000)

        Write.Print(f'[#] By closing this program the bots will leave the game.', Colors.yellow, interval=0.0000)
        exit(1)
    except KeyboardInterrupt:
        print(f'{Colors.white}')
        clear()
        exitVal = True
        exit(1)
    except:
        if not exitVal:
            main()
if not exitVal:
    main()
