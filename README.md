# Pyamaze 수업 정리


```
# turtle02
from pyamaze import maze

m=maze()
m.CreateMaze()
m.run()
```

<img width="509" height="508" alt="image" src="https://github.com/user-attachments/assets/0dad89de-2575-4526-b04c-0629407d7e61" />




코드를 실행하게 되면 그림과 같이 10x10 크기의 미로가 생성된다. 미로의 크기를 설정하는 구문은 m = maze(x,y)이므로 5x5크기로 변경하려면 m = maze(5,5)로 바꿔야한다. 미로의 좌표는 아래의 사진과 같이 구성되어있다.


<img width="508" height="514" alt="image" src="https://github.com/user-attachments/assets/ecbf4a58-47df-4a04-ab0a-d6319528c38b" />



```
from pyamaze import maze,COLOR,agent

m=maze(10,10)
m.CreateMaze(theme=COLOR.light)
a=agent(m)
m.run()
```
- 미로의 배경 색을 변경하기 위해선 COLOR를 import시키고 m.CreateMaze구문으로 배경색을 설정해야한다.

```
from pyamaze import maze,agent
m=maze(20,20)
m.CreateMaze(loopPercent=50)
a=agent(m,filled=True,footprints=True)
m.tracePath({a:m.path})
m.run()
```
- 위 코드는 agent의 발자취를 확인하는 것이다. Agent가 시작점에서 종점까지 이동하는 길을 눈으로 보기 쉽게 구현했다.



미로에서 탈출하는 길을 빠르게 찾는 방법 중 하나인 오른손 법칙을 분석하겠다. 먼저 아래의 코드에서 def구문으로 분석해보겠다.

```
# 벽 따라가기 알고리즘 구현 (def위주로 코드 분석)
def wall_following_algorithm(maze_obj):
    
    def can_move_to(from pos, direction):
        ''' 현재 위치에서 목표점까지 직진할 수 있는지 확인'''
        
    def get_next_position(pos, direction):
        ''' 현재 위치에서 특정 방향으로 이동했을 때의 다음 위치를 반환'''
    
    def can_go_to_goal_directly():
        ''' 현재 위치에서 목표점까지 직진할 수 있는지 확인'''
        
    def get_wall_following_direction():
        ''' 오른손 법칙에 따라 다음 이동방향 결정'''
        
    def move_toward_goal():
        ''' 목표점을 향해 직진'''
```
- 오른손 법칙의 코드 작성 중 중요한 부분은 이 5가지인데 첫 번째로 def can_move_to(from pos, direction): 으로 현재 위치에서 목표점까지 직진할 수 있는지 확인을 한다.
- def get_next_position(pos, direction): 구문으로 그 다음 위치로 이동했을 때 위치를 반환한다.
- def can_go_to_goal_directly():는 직진 가능 여부를 확인하고,
- def get_wall_following_direction():으로 현재위치에서 오른쪽에 벽이 있으면 전진하고 없으면 오른쪽으로 도는 작업을 수행한다.
- 마지막으로 다 확인했으면 def move_toward_goal(): 을 통해 목표점까지 직진한다.

