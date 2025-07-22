# turtle02
from pyamaze import maze

m.CreateMaze(theme=COLOR.light)
a=agent(m,filled=True,footprints=True)
m.tracePath({a:m.path})
m.run()

# loopPercent: 복잡성 나타냄

# pattern='v': 벽이 이어지게끔 생성

# COLOR와 agent는 import구문에 추가

# a.position=(x,y)로 agent를 여러개 생성 가능

# m.tracePath({a:m.path})로 agent의 흔적을 볼 수 있음
