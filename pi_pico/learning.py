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
        room_score = -1
        for state in range(len(self.R)):
            for action in range(len(self.R)):
                room_score = self.R[state][action]
                if room_score == -1:
                    continue
                
                qMax = max(self.Q[action])
                self.Q[state][action] = self.R[state][action] + self.RATE * qMax

    def printQ(self):
        for i in self.Q:
            print(i)
            
            

if __name__ == '__main__':
    start_time = time.ticks_ms()
    learn = Learning()
    for i in range(10000):
        learn.learn()
    #learn.printQ()
    end_time = time.ticks_ms()
    print("runtime %f milliseconds" % (end_time-start_time))
