import random
from modules import *
from sys import exit

class ROULETTE:
    def __init__(self, r_type, modes):
        self.modes = modes
        self.last_bet = 0
        self.martin_type = ''
        self.martin_count = 0
        self.last_bet = 0
        self.now_bet = 0
        self.next_bet = 0
        self.max_bet = 0
        self.summary_dol = self.modes.getint('having_dol')
        self.summary_dol_min = self.modes.getint('having_dol')
        self.even_count = 0
        self.odd_count = 0
        self.red_count = 0
        self.black_count = 0
        self.under18_count = 0
        self.over19_count = 0
        self.now_number = 0
        self.now_color = ''
        self.maxMartin_count = 0
        self.overMartin_count = 0
        self.now_count = 0

        _, self.roulette = readConfigSection('roulettes.ini', r_type)

    def roulette_turn(self):
        now_number, now_color = random.choice(list(self.roulette.items()))
        self.now_number = int(now_number)
        self.now_color = now_color
        return self.now_number, self.now_color

    def judgeing(self, judge_type):
        if self.now_color == 'X':
            self.under18_count = 0
            self.over19_count = 0
            self.even_count = 0
            self.odd_count = 0
            self.red_count = 0
            self.black_count = 0
        else:
            if judge_type == 'underover':
                if self.now_number >= 19:
                    self.over19_count += 1
                    if self.maxMartin_count < self.over19_count:
                        self.maxMartin_count = self.over19_count
                    self.under18_count = 0
                else:
                    self.under18_count += 1
                    if self.maxMartin_count < self.under18_count:
                        self.maxMartin_count = self.under18_count
                    self.over19_count = 0
            elif judge_type == 'evenodd':
                if not self.now_number % 2:
                    self.even_count += 1
                    if self.maxMartin_count < self.even_count:
                        self.maxMartin_count = self.even_count
                    self.odd_count = 0
                else:
                    self.odd_count += 1
                    if self.maxMartin_count < self.odd_count:
                        self.maxMartin_count = self.odd_count
                    self.even_count = 0
            elif judge_type == 'redblack':
                if self.now_color == 'R':
                    self.red_count += 1
                    if self.maxMartin_count < self.red_count:
                        self.maxMartin_count = self.red_count
                    self.black_count = 0
                elif self.now_color == 'B':
                    self.black_count += 1
                    if self.maxMartin_count < self.black_count:
                        self.maxMartin_count = self.black_count
                    self.red_count = 0

    def isChance(self, modes):
        martin_start = self.modes.getint('martin_start')
        if self.martin_type == '':
            if modes.get('priority1') == 'underover':
                if self.under18_count >= martin_start:
                    self.martin_type = 'under18'
                    self.now_count = self.under18_count
                elif self.over19_count >= martin_start:
                    self.martin_type = 'over19'
                    self.now_count = self.over19_count
                if modes.get('priority2') == 'evenodd':
                    if self.even_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                        elif self.now_count < self.even_count:
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                    elif self.odd_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                        elif self.now_count < self.odd_count:
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                    if self.red_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                        elif self.now_count < self.red_count:
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                    elif self.black_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                        elif self.now_count < self.black_count:
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                elif modes.get('priority2') == 'redblack':
                    if self.red_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                        elif self.now_count < self.red_count:
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                    elif self.black_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                        elif self.now_count < self.black_count:
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                    if self.even_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                        elif self.now_count < self.even_count:
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                    elif self.odd_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                        elif self.now_count < self.odd_count:
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
            elif modes.get('priority1') == 'evenodd':
                if self.even_count >= martin_start:
                    self.martin_type = 'even'
                    self.now_count = self.even_count
                elif self.odd_count >= martin_start:
                    self.martin_type = 'odd'
                    self.now_count = self.odd_count
                if modes.get('priority2') == 'underover':
                    if self.under18_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                        elif self.now_count < self.under18_count:
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                    elif self.over19_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
                        elif self.now_count < self.over19_count:
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
                    if self.red_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                        elif self.now_count < self.red_count:
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                    elif self.black_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                        elif self.now_count < self.black_count:
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                elif modes.get('priority2') == 'redblack':
                    if self.red_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                        elif self.now_count < self.red_count:
                            self.martin_type = 'red'
                            self.now_count = self.red_count
                    elif self.black_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                        elif self.now_count < self.black_count:
                            self.martin_type = 'black'
                            self.now_count = self.black_count
                    if self.under18_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                        elif self.now_count < self.under18_count:
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                    elif self.over19_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
                        elif self.now_count < self.over19_count:
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
            elif modes.get('priority1') == 'redblack':
                if self.red_count >= martin_start:
                    self.martin_type = 'red'
                    self.now_count = self.red_count
                elif self.black_count >= martin_start:
                    self.martin_type = 'black'
                    self.now_count = self.black_count
                if modes.get('priority2') == 'underover':
                    if self.under18_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                        elif self.now_count < self.under18_count:
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                    elif self.over19_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
                        elif self.now_count < self.over19_count:
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
                    if self.even_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                        elif self.now_count < self.even_count:
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                    elif self.odd_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                        elif self.now_count < self.odd_count:
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                elif modes.get('priority2') == 'evenodd':
                    if self.even_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                        elif self.now_count < self.even_count:
                            self.martin_type = 'even'
                            self.now_count = self.even_count
                    elif self.odd_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                        elif self.now_count < self.odd_count:
                            self.martin_type = 'odd'
                            self.now_count = self.odd_count
                    if self.under18_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                        elif self.now_count < self.under18_count:
                            self.martin_type = 'under18'
                            self.now_count = self.under18_count
                    elif self.over19_count >= martin_start:
                        if self.martin_type == '':
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count
                        elif self.now_count < self.over19_count:
                            self.martin_type = 'over19'
                            self.now_count = self.over19_count

    def betting(self):
        self.martin_count += 1
        if self.now_bet == 0:
            next_bet = self.modes.getfloat('bet_dol')
        else:
            next_bet = self.now_bet * 2 + self.modes.getfloat('grand_martin_dol')
        self.summary_dol -= next_bet
        if self.summary_dol_min > self.summary_dol:
            self.summary_dol_min = self.summary_dol
        if self.summary_dol <= 0:
            return 'completely_lose'
        else:
            self.now_bet = next_bet
            if self.now_bet > self.max_bet:
                self.max_bet = self.now_bet
        return ''

    def win(self):
        self.martin_count = 0
        self.martin_type = ''
        self.summary_dol += self.now_bet * 2
        self.now_bet = 0

    def overMartin(self):
        self.martin_count = 0
        self.martin_type = ''
        self.now_bet = 0
        self.overMartin_count += 1

    def completelyLose(self):
        print(f'maxMartin is {self.maxMartin_count}')
        print(f'overMartin is {self.overMartin_count}')
        print(f'max_bet = {self.max_bet}')
        exit('completely_lose')

def main():
    _, modes = readDefault('mode.ini')
    r = ROULETTE('EUROPEAN', modes)
    for i in range(modes.getint('calculate_round')):
        number, color = r.roulette_turn()
        #print(f'{str(i+1):5}: {number}, {color}')

        r.judgeing(modes.get('priority1'))
        r.judgeing(modes.get('priority2'))
        r.judgeing(modes.get('priority3'))

        r.isChance(modes)

        if r.martin_type != '':
            if r.martin_type == 'under18':
                if r.under18_count != 0 and r.martin_count <= modes.getint('songiri_times'):
                    ret = r.betting()
                    if ret == 'completely_lose':
                        r.completelyLose()
                elif r.under18_count == 0:
                    r.win()
                else:
                    r.overMartin()
            elif r.martin_type == 'over19':
                if r.over19_count != 0 and r.martin_count <= modes.getint('songiri_times'):
                    ret = r.betting()
                    if ret == 'completely_lose':
                        r.completelyLose()
                elif r.over19_count == 0:
                    r.win()
                else:
                    r.overMartin()
            elif r.martin_type == 'even':
                if r.even_count != 0 and r.martin_count <= modes.getint('songiri_times'):
                    ret = r.betting()
                    if ret == 'completely_lose':
                        r.completelyLose()
                elif r.even_count == 0:
                    r.win()
                else:
                    r.overMartin()
            elif r.martin_type == 'odd':
                if r.odd_count != 0 and r.martin_count <= modes.getint('songiri_times'):
                    ret = r.betting()
                    if ret == 'completely_lose':
                        r.completelyLose()
                elif r.odd_count == 0:
                    r.win()
                else:
                    r.overMartin()
            elif r.martin_type == 'red':
                if r.red_count != 0 and r.martin_count <= modes.getint('songiri_times'):
                    ret = r.betting()
                    if ret == 'completely_lose':
                        r.completelyLose()
                elif r.red_count == 0:
                    r.win()
                else:
                    r.overMartin()
            elif r.martin_type == 'black':
                if r.black_count != 0 and r.martin_count <= modes.getint('songiri_times'):
                    ret = r.betting()
                    if ret == 'completely_lose':
                        r.completelyLose()
                elif r.black_count == 0:
                    r.win()
                else:
                    r.overMartin()

        #print(f'{str(i+1):5}: martin_type = {r.martin_type}')
        #print(f'{str(i+1):5}: martin_count = {r.martin_count}')
        #print(f'{str(i+1):5}: now_bet = {r.now_bet}')
        #print(f'{str(i+1):5}: summary_dol = {r.summary_dol}')
    print(f'maxMartin is {r.maxMartin_count}')
    print(f'overMartin is {r.overMartin_count}')
    print(f'summary_dol = {r.summary_dol}')
    print(f'summary_dol_min = {r.summary_dol_min}')
    print(f'max_bet = {r.max_bet}')

if __name__ == '__main__':
    for _ in range(5):
        main()
        print('*' * 50)
