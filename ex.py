# pyamaze 라이브러리 설치 필요: pip install pyamaze
from pyamaze import maze, agent, COLOR

# 미로 크기 설정
MAZE_ROWS = 10
MAZE_COLS = 10

# 벽 따라가기 알고리즘 구현
def wall_following_algorithm(maze_obj):
    """
    벽 따라가기 알고리즘으로 미로를 해결합니다.
    
    Args:
        maze_obj: pyamaze의 maze 객체
        
    Returns:
        dict: 경로 정보 {현재위치: 다음위치}
    """
    
    # 시작점과 목표점 설정
    start = (maze_obj.rows, maze_obj.cols)  # 시작점 (오른쪽 하단)
    goal = (1, 1)  # 목표점 (왼쪽 상단)
    
    # 방향 정의: 동, 서, 남, 북
    directions = {
        'E': (0, 1),   # 동쪽
        'W': (0, -1),  # 서쪽
        'S': (1, 0),   # 남쪽
        'N': (-1, 0)   # 북쪽
    }
    
    # 오른손 법칙을 위한 방향 순서 (시계방향)
    right_hand_order = ['N', 'E', 'S', 'W']
    
    # 현재 상태 변수
    current_pos = start
    path = {}
    visited = set()
    following_wall = False
    current_direction = 'N'  # 처음에는 북쪽(목표점 방향)을 향함
    
    def can_move_to(from_pos, direction):
        """특정 방향으로 이동할 수 있는지 확인합니다."""
        # 미로 경계 확인
        if from_pos not in maze_obj.maze_map:
            return False
        
        # 해당 방향으로 벽이 있는지 확인 (1이면 이동 가능, 0이면 벽)
        return maze_obj.maze_map[from_pos][direction] == 1
    
    def get_next_position(pos, direction):
        """현재 위치에서 특정 방향으로 이동했을 때의 다음 위치를 반환합니다."""
        row, col = pos
        d_row, d_col = directions[direction]
        next_pos = (row + d_row, col + d_col)
        
        # 미로 범위 내에 있는지 확인
        if (1 <= next_pos[0] <= maze_obj.rows and 
            1 <= next_pos[1] <= maze_obj.cols):
            return next_pos
        return None
    
    def can_go_to_goal_directly():
        """현재 위치에서 목표점까지 직진할 수 있는지 확인합니다."""
        # 현재 위치에서 목표점까지의 경로를 체크
        temp_pos = current_pos
        
        while temp_pos != goal:
            # 목표점 방향 계산
            row_diff = goal[0] - temp_pos[0]  # 음수면 북쪽으로
            col_diff = goal[1] - temp_pos[1]  # 음수면 서쪽으로
            
            # 우선순위: 행을 먼저 맞추고, 그 다음 열을 맞춤
            next_direction = None
            if row_diff < 0:  # 북쪽으로 가야 함
                next_direction = 'N'
            elif row_diff > 0:  # 남쪽으로 가야 함
                next_direction = 'S'
            elif col_diff < 0:  # 서쪽으로 가야 함
                next_direction = 'W'
            elif col_diff > 0:  # 동쪽으로 가야 함
                next_direction = 'E'
            else:
                return True  # 이미 목표점에 도달
            
            # 해당 방향으로 이동할 수 있는지 확인
            if not can_move_to(temp_pos, next_direction):
                return False
            
            # 다음 위치로 이동
            temp_pos = get_next_position(temp_pos, next_direction)
            if temp_pos is None:
                return False
        
        return True
    
    def get_wall_following_direction():
    
        idx = right_hand_order.index(current_direction)

        # 오른쪽, 직진, 왼쪽, 뒤쪽 순서
        check_orders = [
            (idx + 1) % 4,  # 오른쪽
            idx,            # 직진
            (idx - 1) % 4,  # 왼쪽
            (idx + 2) % 4   # 뒤쪽
        ]

        for check_idx in check_orders:
            check_direction = right_hand_order[check_idx]
            if can_move_to(current_pos, check_direction):
                return check_direction

        return current_direction

    
    def move_toward_goal():
        """목표점을 향해 직진합니다."""
        row_diff = goal[0] - current_pos[0]  # 음수면 북쪽
        col_diff = goal[1] - current_pos[1]  # 음수면 서쪽
        
        # 우선순위: 행을 먼저 맞추고, 그 다음 열을 맞춤
        if row_diff < 0 and can_move_to(current_pos, 'N'):
            return 'N'
        elif row_diff > 0 and can_move_to(current_pos, 'S'):
            return 'S'
        elif col_diff < 0 and can_move_to(current_pos, 'W'):
            return 'W'
        elif col_diff > 0 and can_move_to(current_pos, 'E'):
            return 'E'
        
        # 직진할 수 없으면 None 반환
        return None
    
    # 메인 루프
    step_count = 0
    max_steps = MAZE_ROWS * MAZE_COLS * 10  # 최대 이동 횟수
    
    print(f"시작: {start} → 목표: {goal}")
    
    while current_pos != goal and step_count < max_steps:
        # 1. 현재 위치를 visited에 추가
        visited.add(current_pos)
        
        # 다음 이동할 방향과 위치 결정
        next_direction = None
        next_pos = None
        
        # 2. 벽 따라가기 모드가 아닐 때
        if not following_wall:
            # 목표점으로 직진할 수 있는지 확인
            if can_go_to_goal_directly():
                next_direction = move_toward_goal()
                if next_direction is not None:
                    next_pos = get_next_position(current_pos, next_direction)
                    print(f"Step {step_count + 1}: 직진 모드 - {current_pos} → {next_pos} ({next_direction})")
                else:
                    # 직진할 수 없으면 벽 따라가기 모드로 전환
                    following_wall = True
                    print(f"Step {step_count + 1}: 직진 불가! 벽 따라가기 모드로 전환")
            else:
                # 목표점까지 직선 경로가 막혀있으면 벽 따라가기 모드로 전환
                following_wall = True
                print(f"Step {step_count + 1}: 직선 경로 막힘! 벽 따라가기 모드로 전환")
        
        # 3. 벽 따라가기 모드일 때
        if following_wall:
            # 먼저 목표점으로 직진할 수 있는지 다시 확인
            if can_go_to_goal_directly():
                following_wall = False
                next_direction = move_toward_goal()
                if next_direction is not None:
                    next_pos = get_next_position(current_pos, next_direction)
                    print(f"Step {step_count + 1}: 벽 따라가기 → 직진 모드로 전환 - {current_pos} → {next_pos} ({next_direction})")
            else:
                # 오른손 법칙으로 다음 방향 결정
                next_direction = get_wall_following_direction()
                next_pos = get_next_position(current_pos, next_direction)
                current_direction = next_direction  # 현재 방향 업데이트
                print(f"Step {step_count + 1}: 벽 따라가기 - {current_pos} → {next_pos} ({next_direction})")
        
        # 4. 이동할 위치가 결정되지 않았으면 종료
        if next_pos is None:
            print("더 이상 이동할 수 없습니다!")
            break
        
        # 5. path에 경로 저장
        path[current_pos] = next_pos
        
        # 6. 현재 위치를 다음 위치로 업데이트
        current_pos = next_pos
        
        # 7. step_count 증가
        step_count += 1
        
        # 무한루프 방지
        if len(visited) > MAZE_ROWS * MAZE_COLS * 3:
            print("너무 많이 돌아다녔습니다. 무한루프 가능성이 있습니다.")
            break
    
    if current_pos == goal:
        print(f"🎉 목표점에 도달했습니다! ({step_count}단계)")
        print(f"총 방문한 셀 수: {len(visited)}")
        print(f"경로 효율성: {len(path)}/{MAZE_ROWS * MAZE_COLS} = {len(path)/(MAZE_ROWS * MAZE_COLS)*100:.1f}%")
    else:
        print(f"❌ 목표점에 도달하지 못했습니다. (최대 {max_steps}단계)")
    
    return path

def main():
    """메인 실행 함수"""
    # 미로 생성
    m = maze(MAZE_ROWS, MAZE_COLS)
    m.CreateMaze(loopPercent=0, theme=COLOR.light)  # Perfect Maze (해가 1개)
    
    # 벽 따라가기 알고리즘 실행
    print("벽 따라가기 알고리즘 실행 중...")
    print("=" * 50)
    
    solution_path = wall_following_algorithm(m)
    
    print("=" * 50)
    
    # 에이전트 생성 및 경로 표시
    if solution_path:
        # 해결된 경우
        a = agent(m, footprints=True, color=COLOR.blue, filled=True, shape='arrow')
        m.tracePath({a: solution_path}, delay=200)
        print("파란색 화살표가 벽 따라가기 알고리즘의 해입니다.")
        print("화살표를 따라가면서 오른손 법칙이 어떻게 적용되는지 관찰해보세요!")
    else:
        # 해결되지 않은 경우
        a = agent(m, color=COLOR.red)
        print("알고리즘 실행에 실패했습니다.")
    
    # 최적 경로와 비교 (참고용)
    if hasattr(m, 'path') and m.path:
        optimal_agent = agent(m, color=COLOR.green, filled=False, shape='square')
        print(f"초록색 사각형: 최적 경로 (길이: {len(m.path)})")
        print(f"파란색 화살표: 벽 따라가기 경로 (길이: {len(solution_path)})")
        if len(solution_path) > 0:
            efficiency = len(m.path) / len(solution_path) * 100
            print(f"경로 효율성: {efficiency:.1f}%")
    
    # 미로 실행
    m.run()

# 프로그램 실행
if __name__ == "__main__":
    print("벽 따라가기 알고리즘 - Pyamaze")
    print("=" * 40)
    print("설치 방법: pip install pyamaze")
    print("목표: 오른쪽 하단에서 왼쪽 상단까지 벽을 따라가면서 도달")
    print("알고리즘: 오른손 법칙 (Right-hand Rule)")
    print("=" * 40)
    main()