# turtle02
from pyamaze import maze,COLOR,agent

m=maze(10,10)
m.CreateMaze(theme=COLOR.light)
a=agent(m)
m.run()

# loopPercent: 복잡성 나타냄

# pattern='v': 벽이 이어지게끔 생성

# COLOR와 agent는 import구문에 추가 
