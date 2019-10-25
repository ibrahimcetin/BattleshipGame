from socket import socket, AF_INET, SOCK_STREAM
import pickle
import random
import sys

def PvP():
    server = socket(AF_INET, SOCK_STREAM)
    try:
        server.connect(("", 2001))
    except:
        print("Please make sure you turn on the server and check your connection settings.")
        sys.exit()

    ship_coordinates = []
    coordinates = [" " for i in range(100)]
    coordinate_value = {"A":0, "B":10, "C":20, "D":30, "E":40, "F":50, "G":60, "H":70, "I":80, "J":90}

    player1_shot = 0
    player2_shot = 0

    def field():
        return ("""
           player1: {}            player2: {}

         0   1   2   3   4   5   6   7   8   9
       -----------------------------------------
    A  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    B  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    C  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    D  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    E  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    F  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    G  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    H  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    I  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    J  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
        """.format(player1_shot, player2_shot, *coordinates))

    def start(coordinates):
        print(field())
        print("Place your ships")

        i = 0
        while i < 20:
            coordinate = input("Coordinate: ")

            if (len(coordinate) < 2) or (len(coordinate) > 2) or (coordinate[0] not in "ABCDEFGHIJ") or (coordinate[1] not in "1234567890"):
                print("Please enter a letter between A-J first and then enter a number between 0-9. Sample: D6")
                continue
            
            if coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] != " ":
                print("There are already ship in there!")
                continue

            ship_coordinates.append(coordinate)
            coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] = "X"
            
            print(field())
            
            i+=1

        server.send(pickle.dumps(ship_coordinates))

    start(coordinates)
    
    coordinates = [" " for i in range(100)] # clear field
    print(field())
    print("Please wait other player")

    while True:
        data = pickle.loads(server.recv(1024))

        if data[0] == "ready": 
            coordinate = input("Coordinate: ")
            if (len(coordinate) < 2) or (len(coordinate) > 2) or (coordinate[0] not in "ABCDEFGHIJ") or (coordinate[1] not in "1234567890"):
                print("Please enter a letter between A-J first and then enter a number between 0-9. Sample: D6")
                continue

            if coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] != " ":
                print("You already shot it!")
                continue
        
            server.send(bytes(coordinate, "utf-8"))
            data = pickle.loads(server.recv(1024))
        
            coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] = data[0]
            
            player1_shot = data[1]
            player2_shot = data[2]

            print(field())
            print("Please wait other player")
        
        elif data[0] == "refresh":
            player1_shot = data[1]
            player2_shot = data[2]

            print(field())
            print("Please wait other player")

        else:
            player1_shot = data[1]
            player2_shot = data[2]
            
            print(field())
            print(data[0]) # print winner


def PvC():
    player_ship_coordinates = []
    csc = [] # computer_ship_coordinates
    coordinates = [" " for i in range(100)]
    coordinate_value = {"A":0, "B":10, "C":20, "D":30, "E":40, "F":50, "G":60, "H":70, "I":80, "J":90}

    player_shot = 0
    computer_shot = 0

    def char_range(c1, c2):
        for c in range(ord(c1), ord(c2)):
            yield chr(c)

    def field():                                                                                return ("""
           player: {}             computer: {}

         0   1   2   3   4   5   6   7   8   9
       -----------------------------------------
    A  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    B  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    C  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    D  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    E  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    F  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    G  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    H  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    I  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
    J  | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |
       -----------------------------------------
        """.format(player_shot, computer_shot, *coordinates))

    def start(coordinates):
        print(field())
        print("Place your ships")

        i = 0
        while i < 20:
            coordinate = input("Coordinate: ")

            if (len(coordinate) < 2) or (len(coordinate) > 2) or (coordinate[0] not in "ABCDEFGHIJ") or (coordinate[1] not in "1234567890"):
                print("Please enter a letter between A-J first and then enter a number between 0-9. Sample: D6")
                continue

            if coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] != " ":
                print("There are already ship in there!")
                continue
            
            player_ship_coordinates.append(coordinate)
            coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] = "X"
            
            print(field())
            
            i+=1

    def ai_start():
        # 4 block length ship x 1
        for i in range(1):
            direction = random.choice(["h", "v"])
            
            if direction == "h":
                # selectable coordinates for 4 block length ship (horizontal)
                selectable_coordinates = []
                for char in char_range("A", "K"):
                    for j in range(0, 7):
                        selectable_coordinates.append(char+str(j))
                ###

                start_coordinate = random.choice(selectable_coordinates)
                csc.append(start_coordinate)
                csc.append(start_coordinate[0]+str(int(start_coordinate[1])+1))
                csc.append(start_coordinate[0]+str(int(start_coordinate[1])+2))
                csc.append(start_coordinate[0]+str(int(start_coordinate[1])+3))

            if direction == "v":
                # selectable coordinates for 4 block length ship (vertical)
                selectable_coordinates = []
                for char in char_range("A", "H"):
                    for j in range(0, 10):
                        selectable_coordinates.append(char+str(j))
                ###
                
                start_coordinate = random.choice(selectable_coordinates)
                csc.append(start_coordinate)
                csc.append(chr(ord(start_coordinate[0])+1)+start_coordinate[1])
                csc.append(chr(ord(start_coordinate[0])+2)+start_coordinate[1])
                csc.append(chr(ord(start_coordinate[0])+3)+start_coordinate[1])
        ###

        # 3 block length ship x 2
        for i in range(2):
            direction = random.choice(["h", "v"])

            if direction == "h":
                # selectable coordinates for 3 block length ship (horizontal)
                selectable_coordinates = []
                for char in char_range("A", "K"):
                    for j in range(0, 8):
                        selectable_coordinates.append(char+str(j))

                for coo in csc:
                    try:
                        selectable_coordinates.remove(coo)
                    except:
                        continue
                ###
                
                while True:
                    start_coordinate = random.choice(selectable_coordinates)
                    c0 = start_coordinate # coordinate0
                    c1 = start_coordinate[0]+str(int(start_coordinate[1])+1) # coordinate1
                    c2 = start_coordinate[0]+str(int(start_coordinate[1])+2) # coordinate2

                    if (c1 in csc) or (c2 in csc):
                        continue

                    else:
                        csc.append(c0)
                        csc.append(c1)
                        csc.append(c2)
                        break

            if direction == "v":
                # selectable coordinates for 3 block length ship (vertical)
                selectable_coordinates = []
                for char in char_range("A", "I"):
                    for j in range(0, 10):
                        selectable_coordinates.append(char+str(j))

                for coo in csc:
                    try:
                        selectable_coordinates.remove(coo)
                    except:
                        continue
                ###
                
                while True:
                    start_coordinate = random.choice(selectable_coordinates)
                    c0 = start_coordinate # coordinate0
                    c1 = chr(ord(start_coordinate[0])+1)+start_coordinate[1] # coordinate1
                    c2 = chr(ord(start_coordinate[0])+2)+start_coordinate[1] # coordinate2

                    if (c1 in csc) or (c2 in csc):
                        continue

                    else:
                        csc.append(c0)
                        csc.append(c1)
                        csc.append(c2)
                        break

        ###

        # 2 block length ship x 3
        for i in range(3):
            direction = random.choice(["h", "v"])

            if direction == "h":
                # selectable coordinates for 2 block length ship (horizontal)
                selectable_coordinates = []
                for char in char_range("A", "K"):
                    for j in range(0, 9):
                        selectable_coordinates.append(char+str(j))

                for coo in csc:
                    try:
                        selectable_coordinates.remove(coo)
                    except:
                        continue
                ###
                
                while True:
                    start_coordinate = random.choice(selectable_coordinates)
                    c0 = start_coordinate
                    c1 = start_coordinate[0]+str(int(start_coordinate[1])+1)

                    if (c1 in csc):
                        continue

                    else:
                        csc.append(c0)
                        csc.append(c1)
                        break

            if direction == "v":
                # selectable coordinates for 2 block length ship (vertical)
                selectable_coordinates = []
                for char in char_range("A", "J"):
                    for j in range(0, 10):
                        selectable_coordinates.append(char+str(j))

                for coo in csc:
                    try:
                        selectable_coordinates.remove(coo)
                    except:
                        continue
                ###
                
                while True:
                    start_coordinate = random.choice(selectable_coordinates)
                    c0 = start_coordinate
                    c1 = chr(ord(start_coordinate[0])+1)+start_coordinate[1]

                    if (c1 in csc):
                        continue

                    else:
                        csc.append(c0)
                        csc.append(c1)
                        break
        ###
            
        # 1 block length ship x 4
        for i in range(4):
            # selectable coordinates for 1 block length ship
            selectable_coordinates = []
            for char in char_range("A", "K"):
                for j in range(0, 10):
                    selectable_coordinates.append(char+str(j))

            for coo in csc:
                try:
                    selectable_coordinates.remove(coo)
                except:
                    continue
            ###
            
            start_coordinate = random.choice(selectable_coordinates)
            csc.append(start_coordinate)
        ###

    start(coordinates)
    ai_start()
   
    coordinates = [" " for i in range(100)] # clear field
    print(field())
    print("Battle")

    selectable_coordinates = []
    while True:
        # player
        coordinate = input("Coordinate: ")
        
        if (len(coordinate) < 2) or (len(coordinate) > 2) or (coordinate[0] not in "ABCDEFGHIJ") or (coordinate[1] not in "1234567890"):
            print("Please enter a letter between A-J first and then enter a number between 0-9. Sample: D6")
            continue

        if coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] != " ":
            print("You already shot it!")
            continue
        
        if coordinate in csc:
            char = "X"
            player_shot += 1
        else:
            char = "O"
    
        coordinates[coordinate_value[coordinate[0]]+int(coordinate[1])] = char

        print(field())

        if player_shot == 20:
            print(field())
            print("You win!")
            break
        ###

        # computer
        for char in char_range("A", "K"):
            for j in range(0, 10):
                selectable_coordinates.append(char+str(j))

        coordinate = random.choice(selectable_coordinates)
        selectable_coordinates.remove(coordinate)

        if coordinate in player_ship_coordinates:
            computer_shot += 1
        else:
            pass

        if computer_shot == 20:
            print(field())
            print("Computer win!")
            break



if __name__ == "__main__":
    while True:
        choice = input(
"""[1] Player v Computer
[2] Player v Player
[3] How to play?
[0] Exit
 : """)
        if choice == "0":
            break
        elif choice == "1":
            PvC()
        elif choice == "2":
            PvP()
        elif choice == "3":
            print(
"""
Your ships:
    #### x 1
    ###  x 2
    ##   x 3
    #    x 4

You can place your ships horizontally or vertically. You must enter 20 coordinates in total. After you place all your ships, the playground will be cleared. After clearing the playing field, you can start guessing your opponent's ships. In PVP mode, two players must connect to the server before you start placing your ships. 
    If you can shot a ship, will be 'X'. If you can't shot a ship, will be 'O'.
""")
        else:
            continue
