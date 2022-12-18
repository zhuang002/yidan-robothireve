def readinMap() -> list[list[str]]:
    rows, cols = map(int, input().split(' '))
    myMap = [['.'] * cols for i in range(rows)]
    start = (0, 0)
    cameras = []
    for i in range(rows):
        row = input()
        for j in range(cols):
            myMap[i][j] = row[j]
            if row[j] == 'S':
                start = (i, j)
            if row[j] == 'C':
                cameras.append((i, j))
    return start, cameras, myMap


def mark(camera: tuple[int, int], dRow: int, dCol: int, myMap: list[list[str]], myStep: list[list[int]]) -> None:
    r, c = camera
    while 0 <= r < len(myMap) and 0 <= c < len(myMap[0]) and myMap[r][c] != 'W':
        if myMap[r][c] == '.' or myMap[r][c] == 'S':
            myStep[r][c] = -2
        r += dRow
        c += dCol


def preProcessCameras(myMap: list[list[str]], cameras: list[tuple[int]]) -> list[list[int]]:
    rows = len(myMap)
    cols = len(myMap[0])
    stepMap = [[-1] * cols for i in range(rows)]
    for camera in cameras:
        mark(camera, -1, 0, myMap, stepMap)
        mark(camera, 1, 0, myMap, stepMap)
        mark(camera, 0, -1, myMap, stepMap)
        mark(camera, 0, 1, myMap, stepMap)
    return stepMap


def move(loc: tuple[int, int], dRow: int, dCol: int, myMap: list[list[str]],
         stepMap: list[list[int]], step: int) -> tuple[int, int]:
    r, c = loc
    r += dRow
    c += dCol

    if not (0 <= r <= len(myMap) and 0 <= c <= len(myMap[0])):
        return None

    if stepMap[r][c] != -1:
        return None
    s = myMap[r][c]
    if s == '.':
        stepMap[r][c] = step
        return (r, c)
    if s == 'W':
        return None

    if s == 'U':
        stepMap[r][c] = -2
        return move((r, c), -1, 0, myMap, stepMap, step)
    elif s == 'D':
        stepMap[r][c] = -2
        return move((r, c), 1, 0, myMap, stepMap, step)
    elif s == 'L':
        stepMap[r][c] = -2
        return move((r, c), 0, -1, myMap, stepMap, step)
    elif s == 'R':
        stepMap[r][c] = -2
        return move((r, c), 0, 1, myMap, stepMap, step)


def bfs(start: tuple[int, int], myMap: list[list[str]], stepMap: [list[list[int]]]) -> None:
    if stepMap[start[0]][start[1]] == -1:
        stepMap[start[0]][start[1]] = 0
    else:
        return

    current = [start]
    next = []
    step = 1
    while current:
        for loc in current:
            nextLoc = move(loc, -1, 0, myMap, stepMap, step)
            if nextLoc:
                next.append(nextLoc)
            nextLoc = move(loc, 1, 0, myMap, stepMap, step)
            if nextLoc:
                next.append(nextLoc)
            nextLoc = move(loc, 0, -1, myMap, stepMap, step)
            if nextLoc:
                next.append(nextLoc)
            nextLoc = move(loc, 0, 1, myMap, stepMap, step)
            if nextLoc:
                next.append(nextLoc)
        current = next
        next = []
        step += 1


start, cameras, myMap = readinMap()
stepMap = preProcessCameras(myMap, cameras)
bfs(start, myMap, stepMap)
for i in range(len(myMap)):
    for j in range(len(myMap[0])):
        if myMap[i][j] == '.':
            if stepMap[i][j]>=0:
                print(stepMap[i][j])
            else:
                print(-1)
