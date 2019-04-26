import numpy as np
import time
import os
""" Это моя вариация исполнения задания от Fast sense
Я решил,что самым простым и быстрым способом будет выполнение на логиеских условиях
"""
class world:
    size = (20, 20) # задаю размеры карты
    robot_pose = (18,14) # задаю изначальное положение робота
    map = np.zeros(size, 'int64')
    map[16][7:18] = 1
    map[15][8:17] = 1
    map[14][8:17] = 1  # Создаю базу "Препятствия" со всеми клетками = 1
    map[13][8:15] = 1
    map[12][7:14] = 1
    map[11][8:14] = 1
    map[10][7:14] = 1
    map[9][7:11] = 1
    map[8][7:11] = 1
    map[7][7:15] = 1
    map[6][7:15] = 1
    map[5][7:14] = 1
    map[4][9:12] = 1
    map[3][8:11] = 1
    map[robot_pose] = 10
    # Создаем массив с координатами, заходя в которые мы понимаем, что обошли круг по часовой стрелке
    stop_area = []
    for j in range(-1, 4):
        stop_area.append((robot_pose[0] + j, robot_pose[1]+1))
    def get_local_map(self): # Получаем локальную карту вокруг робота
        R = 1
        local_map = world.map[world.robot_pose[0] - R:world.robot_pose[0] + R+1, world.robot_pose[1] - R:world.robot_pose[1] + R+1]
        #"Вырезаем" кусок из карты
        return local_map
    def get_robot_pose(self): # получаем координаты робота
        return world.robot_pose
    def set_robot_pose(self,x,y): # задаем новые координаты робота
        world.map[world.robot_pose] = 0 # Задаю изначальные координаты = 0
        world.robot_pose = (x,y) # задаю новые координаты равные новым т.е. х и у
        world.map[world.robot_pose] = 10 # задаю значение новых координат = 10, т.е. туда " пришел" робот
        return 0

class robot(world):

    def plan(self):
        local_map = world.get_local_map()
        local_pose = world.get_robot_pose()

        if local_map[1][2] == 1 and local_map[2][1]==1 and local_map[0][1] == 1 and local_map[1][0]==0:
            print('Выхожу из "кармана"')
            # проверка на нестандартную ситуацию, когда он попадает в "карман" и его зацикливает влево-вправо
            time.sleep(0.5)
            world.set_robot_pose(local_pose[0], local_pose[1] - 1)
            os.system('cls||clear')
            print(world.map)
            local_map = world.get_local_map()
            local_pose = world.get_robot_pose()
            if local_map[0][1] == 0:
                next_step = (local_pose[0]-1, local_pose[1])
                return next_step
            elif local_map[1][0]==0:
                next_step = (local_pose[0],local_pose[1]-1)
                return next_step

        elif (local_map[2][2] == 1 or local_map[2][1] == 1) and local_map[1][2] ==0:
            print('На право')
            next_step = (local_pose[0],local_pose[1] + 1)
            return next_step
        elif local_map[2][1] == 0 and (local_map[1][0] == 1 or local_map[2][0]):
            print('Вниз')
            next_step = (local_pose[0] + 1, local_pose[1])
            return next_step
        elif (local_map[0][1] == 1 or local_map[0][0]==1 )and local_map[1][0] == 0 :
            print('На лево')
            next_step = (local_pose[0], local_pose[1] - 1)
            return  next_step
        elif local_map[0][1] == 0:
            print("Вперед")
            next_step = (local_pose[0]-1,local_pose[1])
            return next_step

    def move(self):
        print(world.map)
        next_step = robot.plan()
        world.set_robot_pose(next_step[0],next_step[1])
        if next_step in world.stop_area:
            return 0



world = world()
robot = robot()
print(world.stop_area)
while(True):
    os.system('cls||clear')
    go = robot.move()
    time.sleep(0.5)
    print(' ')
    if go == 0:
       print('Обход закончен')
       break




