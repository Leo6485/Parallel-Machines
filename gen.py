from random import *
from math import *
from copy import deepcopy
import numpy as np


class Individuo:
    def __init__(self, size, chromo=None):
        if not chromo:
            chromo = list(range(size))
            shuffle(chromo)

        self.chromo = chromo
        self.size = size
        self.y = None

    def fit(self, funct):
        self.y, self.chromo = funct(self.chromo)

    def mut(self, prob):
        if random() <= prob:
            i, j = randint(0, self.size - 1), randint(0, self.size - 1)
            self.chromo[i], self.chromo[j] = self.chromo[j], self.chromo[i]

class Ag:
    def __init__(self, size=100, elite_size=2, mut_prob=0.01, cross_prob=1, chromo_size=16, sel_mode=1, funct=lambda x:1):
        self.size = size
        self.population = [Individuo(size=chromo_size) for i in range(size)]
        self.chromo_size = chromo_size

        self.elite_size = elite_size
        self.elite = []

        self.funct = funct
        self.sel_mode = sel_mode
        self.mut_prob = mut_prob
        self.cross_prob = cross_prob
        
        self.data = []

    def update_elite(self):
        self.population.sort(key=lambda x: x.y)
        self.elite = deepcopy(self.population[:self.elite_size])

    @staticmethod
    def w_sample(l, w, k):
        result = []
        ids = range(len(l))
        for _ in range(k):
            x = choices(ids, weights=w, k=1)[0]
            w[x] = 0
            result.append(l[x])

        return result
    
    def roleta(self):
        return choices(self.population, weights=[x.y for x in self.population], k=2)
  
    def torneio(self, k=5):
        pai1 = min(choices(self.population, k=k), key=lambda x: x.y)
        pai2 = min(choices(self.population, k=k), key=lambda x: x.y)
        
        return pai1, pai2

    def cross(self):
        len_ = randint(1, self.chromo_size)

        s_idx = randint(0, self.chromo_size - len_)
        e_idx = s_idx + len_

        if self.sel_mode:
            p1, p2 = self.roleta()
        else:
            p1, p2 = self.torneio()
        
        c1, c2 = p1.chromo, p2.chromo

        o1_m = c2[s_idx:e_idx+1]
        o2_m = c1[s_idx:e_idx+1]

        f = self.chromo_size - len_
        o1_right = [i for i in c1[e_idx+1:] + c1[:e_idx+1] if i not in o1_m][:f]
        o2_right = [i for i in c2[e_idx+1:] + c2[:e_idx+1] if i not in o2_m][:f]

        o1_left = [i for i in c2[:e_idx+1] if i not in o1_m + o1_right]
        o2_left = [i for i in c1[:e_idx+1] if i not in o2_m + o2_right]

        o1 = o1_left + o1_m + o1_right
        o2 = o2_left + o2_m + o2_right

        if random() <= self.cross_prob:
            return Individuo(size=self.chromo_size, chromo=o1), Individuo(size=self.chromo_size, chromo=o2)
        else:
            return p1, p2

    def cross_all(self):
        new_pop = []
        while len(new_pop) < self.size:
            o1, o2 = self.cross()
            new_pop.append(o1)
            new_pop.append(o2)

        self.population = new_pop

    def mut(self):
        for x in self.population:
            x.mut(self.mut_prob)
    
    def local_search(self):
        n = max(1, int(self.size * 0.1))
        amostra = sample(self.population, n)
        for x in amostra:
            if x.y is None: x.fit(self.funct)
            best = x.y
            best_chromo = x.chromo[:]
            for _ in range(10):
                i, j = randint(0, self.chromo_size - 1), randint(0, self.chromo_size - 1)
                x.chromo[i], x.chromo[j] = x.chromo[j], x.chromo[i]
                x.fit(self.funct)
                if x.y < best:
                    best = x.y
                    best_chromo = x.chromo[:]
                else:
                    x.chromo[i], x.chromo[j] = x.chromo[j], x.chromo[i]
            x.chromo = best_chromo
            x.y = best


            
    def show(self):
        if len(self.elite):
            print(f"Melhor fitness: {self.elite[0].y} {len(self.elite[0].chromo)} {self.elite[0].chromo}")
    
    def save_data(self):
        y = [x.y for x in self.population]
        mean = np.mean(y)
        median = np.median(y)
        std = np.std(y)

        self.data.append((self.elite[0].y, max(y), min(y), mean, median, std, self.elite[0].chromo))

    def fit(self, generations):
        for _ in range(generations):
            for individuo in self.population:
                individuo.fit(self.funct)

            self.update_elite()
            self.show()
            self.save_data()
            self.cross_all()
            self.mut()
            self.local_search()
            
            self.population.extend(deepcopy(self.elite))