import os
import time
import msvcrt
from random import randint

clearscreem = lambda : os.system('cls' if os.name in ('nt', 'dos') else 'clear')
names_cpu = ["Josejalisco", "Mariahconh", "housetu", "hiarimomo", "sofkawinner", "lapropiamuñeca", "yisusistheway"]

class player:
    def __init__(self ,nickname: str, score : int):
        self.__nickname = nickname
        self.__score = score
    def get_nickname(self):
        return self.__nickname
    def get_score(self):
        return self.__score
    def set_nickname(self, nickname):
        self.__nickname = nickname
    def set_score(self, score):
        self.__score = score

class score:
    def __init__(self, file : str):
        self.__file = file
        self.__scores = {}
        self.__score()

    def __score(self):
        temp = open(self.__file, 'r')
        temp.readline()
        for line in temp:
            self.__scores[line.split(';')[0]] = int(line.split(';')[1])
        temp.close()

    def print_score(self):
        clearscreem(); print("Scores") 
        for keys in self.__scores:
            print(keys, ":" , self.__scores[keys])
        print("Press any key...")
        msvcrt.getch()

    def update_score(self, scores : dict):
        temp = open(self.__file, 'w')
        temp.write("Nickaname;scores\n")
        for keys in scores:
            temp.write(str(keys)+";"+str(scores[keys])+"\n")
        temp.close()

    def set_file(self, file : str):
        self.__file = file
  
    def get_file(self):
        return self.__file    
    
    def get_score(self):
        return self.__scores

    def set_score(self, scores : dict):
        self.__scores = scores

class driver(player):
    def __init__(self, nickname: str, score : int, numcar : int):
        super().__init__(nickname,score)
        self.__numcar = numcar
    def set_numcar(self, numcar):
        self.__numcar = numcar
    def get_numcar(self):
        return self.__numcar

class car(driver):
    def __init__(self, nickname: str, score : int, numcar : int):
        super().__init__(nickname,score,numcar)
        self.__pos = 0
    def get_pos(self):
        return self.__pos
    def set_pos(self, pos):
        self.__pos = pos
    def move(self, pos):
        self.__pos += pos

class lane:
    def __init__(self, dist : int, num : int):
        self.__dist = dist
        self.__num = num
    def set_dist(self, dist):
        self.__dist = dist
    def get_dist(self):
        return self.__dist
    def set_num(self, num):
        self.__num = num
    def get_num(self):
        return self.__num   

class track:
    def __init__(self,dist : int,cant : int):
        self.__cant = cant
        self.__dist = dist
        self.__lanes = []
        self.__lane()

    def __lane(self):
        for i in range(self.__cant):
            self.__lanes.append(lane(self.__dist, i+1))

    def get_lanes(self):
        return self.__lanes
    
    def get_cant(self):
        return self.__cant
    
    def set_cant(self, cant):
        self.__cant = cant
        self.__lane()

    def get_dist(self):
        return self.__dist
    
    def set_dist(self, dist):
        self.__dist = dist

class game:
    def __init__(self):
        self.__scores = score("scores.txt")
        self.__player = car("nadie", 0 , randint(1,100))
        self.__cpuplayers = []
        self.__track = None
        self.__winner = False
        self.__podium = self.__scores.get_score()

    def welcome(self):
        file = open('welcome.txt', 'r')
        for line in file:
            print(line)
        time.sleep(2)

    def print_menu(self):    
        clearscreem()
        print("Welcome to car-sing")
        print("1. Play")
        print("2. Scores")
        print("3. exit")

    def option_menu(self):
        opc = input("select an option (1,2 or 3):")
        while True:
            if opc in ("1", "2", "3"): return opc
            else:
                self.print_menu()
                opc = input("select an option (1,2 or 3):")

    def menu(self):
        self.print_menu()
        opc = self.option_menu() 
        if opc in ("1","2"): return opc
        else: exit()
    
    def __aux_players(self, players : int):
        if players >= 8: players = 7
        elif players <=1 : players = 2
        return players 
        
    def num_players(self):
        while True:
            try:
                players = int(input("how many players do you want to play (max 8): ")); return self.__aux_players(players)
            except ValueError:
                print("you have to enter a number.")

    def ask_player(self):
        self.__player.set_nickname(input("what's is your namenick: ")); print("Welcome to car-sing ", self.__player.get_nickname())
        num = self.num_players()
        for i in range(num): self.__cpuplayers.append(car(names_cpu[i], 0 ,randint(1, 100)))
        self.__track = track(10000, num+1)
        print("Press any kay to play...");  msvcrt.getch()

    def print_init(self):
        clearscreem()
        file = open('carros.txt', 'r')
        for line in file:
            print(line)
        time.sleep(2)

    def player_turn(self):
        print("press any key to roll the dice...");  msvcrt.getch()
        newpos = randint(1,6)*100
        self.__player.move(newpos)

    def cpu_turn(self):
        for cpu in self.__cpuplayers:
            newpos = randint(1,6)*100
            cpu.move(newpos)

    def print_table(self):
        print("Clear like water, this is the position: "); temp = self.__track.get_lanes() ; cont = 0
        print(self.__player.get_nickname(),':',self.__track.get_dist()-self.__player.get_pos() if self.__player.get_pos() <= 10000 else 0 ,"meters from the finish line at the lane ", temp[cont].get_num()) ; cont +=1
        for cpu in self.__cpuplayers:
            print(cpu.get_nickname(),':',self.__track.get_dist()-cpu.get_pos() if cpu.get_pos() <= 10000 else 0  ,"meters from the finish line at the lane ", temp[cont].get_num()); cont +=1
        print("Press any kay to continue...");  msvcrt.getch()

    def iswinner(self):
        if self.__player.get_pos()>=10000:
            print("you are the winner")
            self.__winner = True
        else:
            for cpu in self.__cpuplayers:
                if cpu.get_pos()>=10000:
                    print("you are a loser")
                    self.__winner = True

    def gaming(self):
        self.print_init()
        while not self.__winner:
            clearscreem()
            self.player_turn(); self.cpu_turn()
            self.iswinner(); self.print_table()

    def update_score(self):
        for cpu in self.__cpuplayers: 
            if cpu in self.__podium: self.__podium[cpu.get_nickname()] =cpu.get_pos() if cpu.get_pos()>self.__podium[cpu.get_nickname()] else self.__podium[cpu.get_nickname()] 
            else: self.__podium[cpu.get_nickname()] =cpu.get_pos()
        if self.__player.get_nickname() in self.__podium: self.__podium[self.__player.get_nickname()] = self.__player.get_pos() if self.__player.get_pos()>self.__podium[self.__player.get_nickname()] else self.__podium[self.__player.get_nickname()]
        else: self.__podium[self.__player.get_nickname()] = self.__player.get_pos()
        self.__scores.update_score(self.__podium)

    def position_players(self):
        my_dict = {self.__player.get_nickname(): self.__player.get_pos()}
        for cpu in self.__cpuplayers: my_dict[cpu.get_nickname()]=cpu.get_pos()
        for i in range(3):
            key_max = max(my_dict.keys(), key=(lambda k: my_dict[k])) ; print(i+1, "is", key_max)
            del my_dict[key_max]

    def podium(self):
        print("this is the champions in car-sing:")
        self.position_players()
        self.update_score()

    def playing(self):
        clearscreem()
        self.ask_player()
        self.gaming()
        self.podium()
        print("Press any kay to continue...");  msvcrt.getch()

    def game(self):
        self.welcome()
        while True:
            opc = self.menu()
            if opc == "1": self.playing()
            else: self.__scores.print_score()
            #time.sleep(2)

if __name__ == '__main__':
    clearscreem()
    play = game()
    play.game()
