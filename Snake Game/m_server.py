#Checking heartbeat 5 sec
#const heartbeat changed
#90 degree rotation
# usero mord pak konim 

#sari she
#user barande dashte bashim
#heartbeat ghat shod bemire 
#mininet for Ali joon
#sizemoon dg sabet nabashe 


import json
import time
import socket 
from timeit import default_timer
from threading import Thread 
from SocketServer import ThreadingMixIn 
import threading
import sys
import select 
from random import randint

deadline = 7

sib=False

board_size = 0


# initial_moving_object_of_board = {
#     'snakes' : [[[0, 0],[1,0],[2,0]]],
#     'food' : [3,1],
# }

new_degree = 0

apples = [[7,8],[4,2],[5,6]]

food = [9,4]
food_num = 1

sockets = []

users = []

new_snakes = [[[0, 0],[1,0],[2,0]], [[9,0],[9,1],[9,2]], [[9,9],[8,9],[7,9]] , [[0,9],[0,8],[0,7]]]

moves = ["down","right","up","left",]

def print_winner():
    min_length = 100
    winners = []
    for user in users:
        if(user.alive):
            print user.username + "length is : ",len(user.snake) 
            #print user.snake
            snake_length=len(user.snake)
            if snake_length <= min_length:
                min_length = snake_length
                winner = user
    for user in users:
        if(user.alive):
            if len(winner.snake)==len(user.snake):
                winners.append(user)
    print "game is over"
    for winer in winners:
        print "winner is "+ winer.username

def rotate(input_map, degree):
    result = {}
    global board_size
    size = board_size-1
    if degree == 0:
        return input_map
    else:
        for field in input_map:
            # print field
            if(field == "snakes"):
                result[field] = []
                # print "in snake's if!"
                for snake in input_map[field]:
                    # print "snake = " , snake
                    new_snake = []
                    for part in snake:      
                        # print "part = " , part
                        temp_x = part[0]
                        temp_y = part[1]
                        if degree == 1:
                            new_snake.append([temp_y, size-temp_x])
                        elif degree == 2:
                            new_snake.append([size-temp_x,size-temp_y])
                        elif degree == 3:
                            new_snake.append([size-temp_y,temp_x])
                    result[field].append(new_snake)
                # print result[field]
            elif(field == "food"):
                # print "in food's if"
                temp_x = input_map[field][0]
                temp_y = input_map[field][1]
                if degree == 1:
                    result[field] = [temp_y, size-temp_x]
                elif degree == 2:
                    result[field] =[size-temp_x,size-temp_y]
                elif degree == 3:
                    result[field] =[size-temp_y,temp_x]
                # print result[field]
            elif(field == "obstacles" or field == "remove"):
                result[field] = []
                for part in input_map[field]:   
                    # print "part = ", part
                    temp_x = part[0]
                    temp_y = part[1]
                    if degree == 1:
                        result[field].append([temp_y, size-temp_x])
                    elif degree == 2:
                        result[field].append([size-temp_x,size-temp_y])
                    elif degree == 3:
                        result[field].append([size-temp_y,temp_x])
                # print result[field] 
            elif(field == "size"):
                result[field]=input_map[field]        
    return result            

def find_degree(socket):
    for user in users:
        if socket == user.sock:
            return user.degree,user.username

def check_heartbeats():
    #print "check_heartbeats"
    #print time.time()
    for user in users:
        if user.alive:
            # print user.username
            # print user.last_recv
            if ((time.time() - user.last_recv) > 1.5):
                #print time.time() 
                #print user.last_recv
                user.alive = False
                print "user ----" + user.username + "-------is dead"

def check_new_food_position(t_x,t_y):
    no_obstacle = check_obstacle(t_x+1,t_y,"up")
    no_snake = check_snake(t_x+1,t_y,"up","saghar")
    if no_obstacle==False and no_snake==False:
        return True
    else:
        return False

def high_send_moving():
    def send_moving():
        #print "----------- board size ---------------- = ",board_size
        moving_object_of_board= board_generator()
        global food_num
        #print "after board_generator: " ,food_num
        if food_num==16 :
                print_winner()
               # for user in users:
                #    user.sock.close()
                food_num = food_num+1
                #sys.exit()
        #print moving_object_of_board
        for user in users :
            moving_board_obj = rotate(moving_object_of_board,user.degree) 
            try:
                user.sock.send(json.dumps(moving_board_obj))
            except:
                pass
            if(user.alive == False):
                user.snake = [[[],[],[]]]
                del user.snake[:]
                #users.remove(user)
    set_interval(send_moving,2)    

def board_generator():
    def move_snake():
        moving_object_of_board = {
            'snakes' : [],
            'food' : [],
            'remove' : [],
        }
        grw=False
        for user in users:
            user.generate_next_position()
        for user in users:
            #print user.username
            #print user.snake
            if (user.alive) and (user.grow==False):
                moving_object_of_board['snakes'].append(user.snake)
                moving_object_of_board['remove'].append(user.snake[0])
                del user.snake[0]
            elif (user.alive) and (user.grow):
                grw=True
                moving_object_of_board['snakes'].append(user.snake)               
                user.grow = False
            else:
               
                for part in user.snake:
                    moving_object_of_board['remove'].append(part)
        global sib
        if sib==True :
            #print "hellllooooooooooooooooo"
            #moving_object_of_board['remove'].append(food)
            good_pos = False
            while good_pos==False:
                t_x=randint(0,size-1)
                t_y=randint(0,size-1)
                if(check_new_food_position(t_x,t_y)):
                    good_pos=True
                else:
                    good_pos=False

            #print t_x,"--",t_y
            global food
            food=[t_x,t_y]
            global food_num
            food_num=food_num+1
            #print "num == ",food_num
            sib=False
            
            #print "fooooooooooooooooooooooooooooooood = ",food
        moving_object_of_board['food']=food
        return moving_object_of_board
    return move_snake()


def check_obstacle(temp_x,temp_y,move):
    for obstacle in obstacles :
        if move=="up" and obstacle == [temp_x-1, temp_y]:
            return True
        elif move=="right" and obstacle == [temp_x, temp_y+1]:
            return True
        elif move=="down" and obstacle == [temp_x+1, temp_y]:
            return True
        elif move=="left" and obstacle == [temp_x, temp_y-1]:
            return True
    return False

def check_food(temp_x,temp_y,move):
    if move=="up" and food == [temp_x-1, temp_y]:
                return True
    elif move=="right" and food == [temp_x, temp_y+1]:
                return True
    elif move=="down" and food == [temp_x+1, temp_y]:
                return True
    elif move=="left" and food == [temp_x, temp_y-1]:
                return True
    else :
        return False
def out_of_map(temp_x,temp_y,move):
        if move=="up" and temp_x-1==-1 :
            return True
        elif move=="right" and temp_y+1==10:
            return True
        elif move=="down" and temp_x+1==10:
            return True
        elif move=="left" and temp_y-1==-1:
            return True
        else:
            return False
def check_snake(temp_x,temp_y,move,name):
    for user in users :
        for part in user.snake :
            if move=="up" and part == [temp_x-1, temp_y]:
                return True
            elif move=="right" and part == [temp_x, temp_y+1]:
                return True
            elif move=="down" and part == [temp_x+1, temp_y]:
                return True
            elif move=="left" and part == [temp_x, temp_y-1]:
                return True
    return False    


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


class User(object):
    
    def __init__(self,username,snake,move,degree,alive,grow,last_recv,sock):
        self.username = username
        self.snake = snake
        self.move = move
        self.degree = degree
        self.alive = alive
        self.grow = grow
        self.last_recv = last_recv
        self.sock = sock

    def generate_next_move(self):
        temp = 0
        for m in moves :
            if m == self.move :
                index = temp
            temp += 1
        index = (index + self.degree)%4
        self.move = moves[index]

    def generate_next_position(self):
        if(self.alive):
            temp_x = self.snake[-1][0]
            temp_y = self.snake[-1][1]
            #print "temp_y = ",temp_y
            obst = False
            #print "move = ",self.move
            if (check_obstacle(temp_x,temp_y,self.move)==True):
                print self.username + " is dead !!!"
                self.alive=False
                #del self.snake[:]
            elif(check_snake(temp_x,temp_y,self.move,self.username)):
                print self.username + " is dead !!!"
                self.alive=False
            elif(out_of_map(temp_x,temp_y,self.move)):
                print self.username + " is dead !!!"
                self.alive=False
            else:
                if(check_food(temp_x,temp_y,self.move)):
                    for user in users:
                        if user!=self :
                            user.grow=True
                            global sib
                            sib=True
                if self.move == "up":
                    self.snake.append([temp_x-1, temp_y])
                elif self.move == "right":
                    self.snake.append([temp_x, temp_y+1])
                elif self.move == "down":
                    self.snake.append([temp_x+1, temp_y])
                elif self.move == "left":
                    self.snake.append([temp_x, temp_y-1])
        
            
# Multithreaded Python server : TCP Server Socket Thread Pool
class ClientThread(Thread): 
 
    def __init__(self,ip,port1,port2,socket1,socket2): 
        Thread.__init__(self) 
        self.ip = ip 
        self.port1 = port1 
        self.socket1 = socket1
        self.port2 = port2 
        self.socket2 = socket2
        # self.last_recv
        print "[+] New server socket thread started for heartbeat --> " + ip + ":" + str(port1) 
        print "[+] New server socket thread started for data --> " + ip + ":" + str(port2) 
    # def timer(self):
    #     start = default_timer()
    #     while 1:
    #         duration = default_timer() - start
    #         if duration > 7:
    #             self.check_heartbeat()

    # def check_heartbeat(self):
    #     if(default_timer() - last_recv > 7):
    #         print "bishtar az 7 shod"


    def send_map(self):
        #print "---------------------------------- sending board ------------------------------------"
        user_degree,user_username = find_degree(self.socket2)
        #print "for" + user_username
        #print "degree = ",user_degree
        rotated_board = rotate(board,user_degree)
        self.socket2.send(json.dumps(rotated_board))

    def send_initial_moving(self): 
        initial_moving_object_of_board = {
            'snakes' : [],
            'food' : [],
            }
        for user in users:
            initial_moving_object_of_board['snakes'].append(user.snake)
        initial_moving_object_of_board['food']=food
        #print "initial"
        #print initial_moving_object_of_board 
        #print "################################### rotating initial #################################"
        user_degree,user_username = find_degree(self.socket2)
        #print "for "+user_username
        #print user_degree
        rotated_initial = rotate(initial_moving_object_of_board,user_degree)
        #print "################################### sending initial #################################"
        #print rotated_initial
        self.socket2.send(json.dumps(rotated_initial))
        #self.socket2.send(json.dumps(initial_moving_object_of_board))

    def run(self): 
        first = True
        inputs  = [self.socket1,self.socket2]
        outputs = []
        while inputs :
            readable, writable, exceptional = select.select(inputs,outputs,inputs)
            for s in readable:
                if s is self.socket1 :
                    data = self.socket1.recv(2048) 
                    #print  "Server received data:", data
                    if data:
                    # print "some data"
                        load_data = json.loads(data) 
                        #print "username = " + load_data["username"] + "message = " + load_data["message"] + "\n"
                        if(load_data["message"] == "HeartBeat"):
                            for user in users:
                                if user.username == load_data["username"]:
                                    user.last_recv = time.time()
                                    #print user.last_recv , user.username
                            
                            if first:
                            #----------------new degreeeee------------
                                global new_degree 

                                new_snake = []
                                for part in new_snakes[new_degree]:
                                    new_snake.append(part)

                                new_move = moves[new_degree]
                                new_user = User(load_data["username"], new_snake, new_move, new_degree,True,False,time.time(),self.socket2)
                                users.append(new_user)
                                new_degree = (new_degree +1)%4
                                # print "sending map"
                                self.send_map()
                                # print "sending initial moving"
                                self.send_initial_moving()
                                first = False
                                #sockets.append(self.socket2)
                    else:
                        print "no data"
                elif s is self.socket2 : 
                    keystroke = self.socket2.recv(2048)
                    load_keystroke = json.loads(keystroke)
                    #print "keystroke happened for " 
                    #print load_keystroke["username"]
                    #print load_keystroke["action"]
                    for user in users:
                        if user.username==load_keystroke["username"]:
                            user.move=load_keystroke["action"]
                            user.generate_next_move()

            # try:
            #     keystroke = self.socket2.recv(2048)
            #     print "keystroke happened for " + keystroke["username"]
            #     print keystroke["action"]
            # except:
            #     print "excepte keystroke"
            # try:
            #     data = self.socket1.recv(2048) 
            #     print  "Server received data:", data
            
            #     if data:
            #         # print "some data"
            #         load_data = json.loads(data) 
            #         print "username = " + load_data["username"] + "message = " + load_data["message"] + "\n"
            #         if(load_data["message"] == "HeartBeat" and first):
            #             # print "sending map"
            #             self.send_map()
            #             # print "sending initial moving"
            #             self.send_initial_moving()
            #             first = False
            #             sockets.append(self.socket2)
            #     else:
            #         print "no data"
                
            # except:
            #      a = 2


            # last_recv = default_timer()
            
# Multithreaded Python server : TCP Server Socket Program Stub
TCP_IP = "127.0.0.1"
TCP_PORT = 12345
BUFFER_SIZE = 1024  # Usually 1024, but we need quick response 
 

input_file = open("map.txt", "r")
x = 0
y = 0
obstacles = []
for line in input_file:
    for char in line.split(" "):
        if(char == "1"):
            new = [x , y]
            obstacles.append(new)
        y += 1
    x += 1
    y = 0
input_file.close()
size = x
board_size = x

board = {
        'obstacles' : obstacles,
        'size' : size
        }

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
tcpServer.bind((TCP_IP, TCP_PORT)) 
threads = [] 
num_of_players = 0
started = False
while True: 
    tcpServer.listen(4) 
    print "Multithreaded Python server : Waiting for connections from TCP clients..." 
    (conn1, (ip,port1)) = tcpServer.accept()
    (conn2, (ip,port2)) = tcpServer.accept()
    conn1.setblocking(0)
    conn2.setblocking(0)
    num_of_players = num_of_players + 1
    #print 'injaaaaaaaaa'
    newthread = ClientThread(ip,port1,port2,conn1,conn2) 
    newthread.start() 
    threads.append(newthread) 
    if num_of_players >= 2 and started == False:
        started = True
        print 'before send moving'
        high_send_moving()
        print 'after send moving'
        set_interval( check_heartbeats, 0.25)

 
for t in threads: 
    t.join() 
