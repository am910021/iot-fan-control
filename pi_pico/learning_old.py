import time

class Learning:
    def __init__(self):

        self.STATE = ['A', 'B', 'C', 'D', 'E', 'F']
        self.RATE = 0.8
        self.R = [
            [-1, -1, -1, -1, 0, -1],
            [-1, -1, -1, 0, -1, 100],
            [-1, -1, -1, 0, -1, -1],
            [-1, 0, 0, -1, 0, -1],
            [0, -1, -1, 0, -1, 100],
            [-1, 0, -1, -1, 0, 100]
        ]

        self.Q = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]

        self.matrix = [
            [0, 0, 0, 0, 80, 0],
            [0, 0, 0, 64, 0, 100],
            [0, 0, 0, 64, 0, 0],
            [0, 80, 51, 0, 81, 0],
            [64, 0, 0, 64, 0, 100],
            [0, 80, 0, 0, 80, 100]
        ]

    def learn(self):
        # Room B, Action F
        # R(B,F) = 100
        # Q(F,B) Q(F,E) Q(F,F)

        # Room A, Action E
        # R(A, E) = 0
        # Q(E,A) Q(E,D) Q(E,F)

        room_score = -1
        for state in range(len(self.R)):
            for action in range(len(self.R)):
                room_score = self.R[state][action]
                if room_score == -1:
                    continue

                #print("Room %s - State %s" % (self.STATE[state], self.STATE[action]))
                qMax = self.findQMaxByAction2(state, action)
                self.Q[state][action] = self.R[state][action] + self.RATE * qMax
                #print("Q(%s,%s)=%d" % (self.STATE[state], self.STATE[action], self.Q[state][action]))

            #print()

    def findQMaxByAction(self, state: int, action: int):
        targets = []
        values = []
        for i in range(len(self.R)):
            if self.R[action][i] > -1:
                targets.append(i)
                values.append(self.Q[action][i])

        # print("R(%s,%s)=%d, %s" % (
        # self.STATE[state],
        # self.STATE[action],
        # self.R[state][action],
        # " ".join(["Q(%s,%s)=%d" % (self.STATE[action], self.STATE[i], self.Q[action][i]) for i in targets])))
        return max(values)
    
    def findQMaxByAction2(self, state: int, action: int):
        return max(self.Q[action])

    def printQ(self):
        for i in self.Q:
            print(i)







if __name__ == '__main__':
    start_time = time.time()
    learn = Learning()
    for i in range(1000):
        learn.learn()
    learn.printQ()
    end_time = time.time()
    print(end_time-start_time)

