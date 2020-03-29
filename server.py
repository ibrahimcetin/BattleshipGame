from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import pickle
from time import sleep

socket = socket(AF_INET, SOCK_STREAM)
socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
socket.bind(("", 2001))
socket.listen(2)
print("Server running...")

player1, player1_addr = socket.accept() # accept player1
print(f"{player1_addr[0]} has been connected")
player2, player2_addr = socket.accept() # accept player2
print(f"{player2_addr[0]} has been connected")

player1_win = False
player2_win = False

player1_shot = 0
player2_shot = 0

player1_coordinates = pickle.loads(player1.recv(1024)) # recv player1 ship coordinates
player2_coordinates = pickle.loads(player2.recv(1024)) # recv player2 ship coordinates


while True:
    # send ready to player1
    if player2_win:
        player1.send(pickle.dumps(["You lose", player1_shot, player2_shot]))
        player2.send(pickle.dumps(["You win", player1_shot, player2_shot]))
    else:
        player1.send(pickle.dumps(["ready"]))
    ###

    #check player1's shot:
    player1_coordinate = player1.recv(1024).decode("utf-8")
    if player1_coordinate in player2_coordinates:
        player1_shot += 1
        player1.send(pickle.dumps(["X", player1_shot, player2_shot]))
        
        player2.send(pickle.dumps(["refresh", player1_shot, player2_shot]))
        sleep(0.5)
    else:
        player1.send(pickle.dumps(["O", player1_shot, player2_shot]))
    ###

    # check player1 win
    if player1_shot == 20:
        player1_win = True
    ###
    
    # send ready to player2 
    if player1_win:
        player1.send(pickle.dumps(["You win", player1_shot, player2_shot]))
        player2.send(pickle.dumps(["You lose", player1_shot, player2_shot])) 
    else:
        player2.send(pickle.dumps(["ready"]))
    ###

    # check player2's shot
    player2_coordinate = player2.recv(1024).decode("utf-8")
    if player2_coordinate in player1_coordinates:
        player2_shot += 1
        player2.send(pickle.dumps(["X", player1_shot, player2_shot]))
        
        player1.send(pickle.dumps(["refresh", player1_shot, player2_shot]))
        sleep(0.5)
    else:
        player2.send(pickle.dumps(["O", player1_shot, player2_shot]))
    ###

    # check player2 win
    if player2_shot == 20:
        player2_win = True
    ###
