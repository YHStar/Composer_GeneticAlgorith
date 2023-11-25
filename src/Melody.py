from functools import total_ordering
from .Interval import Interval
import random
from copy import deepcopy

@total_ordering
class Melody:
    def __init__(self, notes: list, length=32):
        self.notes = notes
        self.len = length
        self.score = 0     # 适应度
        assert self.len == len(self.notes)
        
    # 更新适应度
    def GetScore(self, function='basic'): 
        lambda1 = 0.5
        lambda2 = 1.0
        # 对所有相邻音程评分，取平均
        interval = Interval()
        note1 = 0
        note2 = 0
        cnt = 0
        score1 = 0
        index = 0
        while self.notes[index] == 0 or self.notes[index] == 28:
            index += 1
        note1 = self.notes[index]
        
        for i in range(index + 1, self.len):
            if self.notes[i] == 0 or self.notes[i] == 28:
                continue
            note2 = self.notes[i]
            score1 += interval.Score_TwoNote(note1, note2)
            cnt += 1
            note1 = note2
        score1 = score1 / cnt
        
        # 旋律中的调内音越多，适应度越好(越低)
        # 统计G大调中的调内音 (G, A, B, C, D, E, F#)
        cnt = 0
        inTonality = 0
        Gmaj = [3, 5, 7, 8, 10, 0, 2]
        for note in self.notes:
            if note > 0 and note < 28:
                cnt += 1
                if (note % 12) in Gmaj:
                    inTonality += 1
        score2 = 1 - inTonality / cnt
        self.score = lambda1 * score1 + lambda2 * score2 
        
    def GetMutation(self, mutationType=0):
        mutation = deepcopy(self)
        # 变异位置
        target = random.randint(0, mutation.len - 1)
        while mutation.notes[target] == 0 or mutation.notes[target] == 28:
            # 无法改变休止，延音
            target = random.randint(0, mutation.len - 1)

        if mutationType == 0:           # 无变异
            return mutation
        
        elif mutationType == 1:         # 八度变异
            upOrDown = random.randint(0, 1)
            upperBound = min(27, mutation.notes[target] + 12)
            lowerBound = max(1, mutation.notes[target] - 12)
            if upOrDown == 0:
                mutation.notes[target] = upperBound
            else:
                mutation.notes[target] = lowerBound
            return mutation
            
        elif mutationType == 2:         # 音符变异
            # 0.03的概率变成延音
            res = random.random()
            if res < 0.03:
                mutation.notes[target] = 28
            else:
                # 在上下五度之间随机变异
                deviation = random.randint(-7, 7)
                mutation.notes[target] += deviation
                if mutation.notes[target] > 27:
                    mutation.notes[target] = 27
                elif mutation.notes[target] < 1:
                    mutation.notes[target] = 1
            return mutation
                    
        elif mutationType == 3:         # 交换音符变异
            target2 = random.randint(0, mutation.len - 1)
            # 这里实际上有可能出现一段旋律只有一个音的情况，直接允许自身交换，也就是没有变异
            while mutation.notes[target2] == 0 or mutation.notes[target2] == 28:
                target2 = random.randint(0, mutation.len - 1)
            note1 = mutation.notes[target]
            note2 = mutation.notes[target2]
            mutation.notes[target] = note2
            mutation.notes[target2] = note1
            return mutation                
    
    def __lt__(self, other):
        return self.score < other.score
    
    def __hash__(self):
        hashcode = 0
        for i in range(self.len):
            hashcode += ((self.notes[i] + i**2) ** 3)
        return hashcode
    
    def __eq__(self, other):
        return self.__hash__() == other.__hash__()