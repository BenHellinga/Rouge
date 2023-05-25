# player: [[x,y],on]
# enemyList: [[x,y,on,ClassEnemy],ect.]
# ====================================================================================================
def genFakePotions():
   mixedPotions = []
   done = 0
   while done < len(potions):
       newl = False
       l = ""
       for r in range(0, 5):
           l += chr(randrange(0, 26) + ord("A"))
       for s in range(0, done):
           if l == potions[s][4]: newl = True
       if newl == False:
           potions[done] += [l]
           done += 1
   return mixedPotions
# ====================================================================================================
from random import randrange
from sys import exit
import math
from colorama import Fore, Style

# print(Fore.GREEN + "R" + Style.RESET_ALL)

floor = 1
enemyList = []

START_XOFF = 0
START_YOFF = 0

PIX_WIDTH = 51
PIX_LENGTH = 31
SCREEN_LENGTH = 91
SCREEN_WIDTH = 41

ROOMS = int(PIX_LENGTH * PIX_WIDTH / 200)
ROOM_FAIL_CHANCE = 3  # 1 in x chance to fail
WALL_CHAR = "#"
PLANT_ROOM_CHANCE = 2
ROOM_PLANT_RNG = 5
STAIR_AMOUNT = int(ROOMS / 30) + 1
STAIR_CHAR = "%"
AIR_CHAR = "_"
ENEMIES = int(ROOMS * 0.8)
TEST_CHAR = "@"

DOOR_CHAR = "+"
TUNNELS = int(ROOMS / 1.5) + 10
TUNNEL_PLANT_RNG = 7

ITEMS = randrange(int(ROOMS / 10) + 1, int(ROOMS / 3) + 1)

DEV = True
GEN_FEEDBACK = True

PLAYER_CHAR = "J"

PLANTS_ON = True
PLANT = "w"
SIGHTLINE_CHAR = "."
UNSEEN_CHAR = " "
SIGHTLINE_ON = False
SIGHT_MEMORY = True
HIDE_ENEMIES = False
COLOR = False
ENEMY_AWAKE_CHANCE = 3
ENEMY_WAKEUP_CHANCE = 3

WAND_CHAR = "/"
SWORD_CHAR = "!"
BOW_CHAR = "("
POTION_CHAR = "Ӈ"
ARMOR_CHAR = "¥"

COINS = 0
MAX_HP = 100
HP = 100
STRENGTH = 5
PLAYER_DAMAGE = 0

inventory = []
equiped = [
   [[SWORD_CHAR, "Shortsword", 2, 40, 3, 1], "weapon"],
   [[ARMOR_CHAR, "Weak Chestplate", 2], "armor"],
   "Empty",
   "Empty"
]

# chr, name, damage, crit chance, crit damage multiplier, range
weapons = [
   [WAND_CHAR, "Wand", 1 * floor, 50, 3, 2],
   [SWORD_CHAR, "Shortsword", int(1.5 * floor), 30, 2, 1],
   [BOW_CHAR, "Bow", 1 * floor, 20, 2, 3],
   [SWORD_CHAR, "Longsword", 2 * floor, 10, 1.5, 1]
]
# chr, name, defence
armors = [
   [ARMOR_CHAR, "Iron Chestplate", 3]
]
# chr, name, effect, discovered
potions = [
   [POTION_CHAR, "Healing", "heal", False],
   [POTION_CHAR, "Critical", "crtical", False],
   [POTION_CHAR, "Damage", "damage", False],
   [POTION_CHAR, "Strength", "strength", False]
]
mixedPotions = genFakePotions()

# chr, name, health, damage, defence, speed, turn
ememies = [
   []
]
# ====================================================================================================
def infoPannel(message):
   for i in range(0, 10):
       print()

   l = ""
   for i in range(1, len(message)):
       if message == [""]: break
       l += message[i] + ", "
   print(l)

   print("Floor: " + str(floor) + ", HP: " + str(HP) + " / " + str(MAX_HP) + ", Coins: " + str(COINS))
# ====================================================================================================
def printDisplay(newpix, seenpix, player, centered):
   replace(newpix, "5", UNSEEN_CHAR)
   replace(newpix, "N", UNSEEN_CHAR)

   x1 = 0
   x2 = len(newpix[0])
   y1 = 0
   y2 = len(newpix)

   if centered == True:
       if len(pix[0]) > SCREEN_LENGTH:
           if player[0][0] - int((SCREEN_LENGTH - 1) / 2) > 0: x1 = player[0][0] - int((SCREEN_LENGTH - 1) / 2)
           if player[0][0] + int((SCREEN_LENGTH - 1) / 2) < len(newpix[0]): x2 = player[0][0] + int(
               (SCREEN_LENGTH - 1) / 2)
           if x1 == 0: x2 = SCREEN_LENGTH - 1
           if x2 == len(pix[0]): x1 = len(pix[0]) - SCREEN_LENGTH

       if len(pix) > SCREEN_WIDTH:
           if player[0][1] - int((SCREEN_WIDTH - 1) / 2) > 0: y1 = player[0][1] - int((SCREEN_WIDTH - 1) / 2)
           if player[0][1] + int((SCREEN_WIDTH - 1) / 2) < len(newpix): y2 = player[0][1] + int((SCREEN_WIDTH - 1) / 2)
           if y1 == 0: y2 = SCREEN_WIDTH - 1
           if y2 == len(pix): y1 = len(pix) - SCREEN_WIDTH

   for y in range(y1, y2):
       line = ""
       for x in range(x1, x2):
           if SIGHTLINE_ON == True:
               if seenpix[y][x] == True:
                   printColor(newpix[y][x].chr, newpix[y][x].color)
               else:
                   print("  ", end="")
           else:
               printColor(newpix[y][x].chr, newpix[y][x].color)
       print()
   return
# ====================================================================================================
def printColor(chr, color):
   print(" ", end="")
   if color == "white":
       print(chr, end="")
   elif color == "green":
       print(Fore.GREEN + chr + Style.RESET_ALL, end="")
   elif color == "grey":
       print(Fore.WHITE + chr + Style.RESET_ALL, end="")
   elif color == "cyan":
       print(Fore.CYAN + chr + Style.RESET_ALL, end="")
   elif color == "orange":
       print(Fore.LIGHTBLUE_EX + chr + Style.RESET_ALL, end="")
   elif color == "yellow":
       print(Fore.YELLOW + chr + Style.RESET_ALL, end="")
   elif color == "red":
       print(Fore.RED + chr + Style.RESET_ALL, end="")
# ====================================================================================================
# removes the 1s from around a box and changes them to 3s
def removeBoxSpawn(pix, middleX, middleY, length, height):
   # gets the top left corner using math from the middle
   startX = int(middleX - (length - 1) / 2 - 3)
   startY = int(middleY - (height - 1) / 2 - 3)

   difX = startX - 1
   difY = startY - 1
   onXEdge = False
   onYEdge = False
   addDifX = 0
   addDifY = 0
   if startX < 0:
       startX = 0
       onXEdge = True
   if startY < 0:
       startY = 0
       onYEdge = True
   difX = startX - difX
   difY = startY - difY
   if onXEdge == True:
       addDifX = difX - 1
   if onYEdge == True:
       addDifY = difY - 1

   # checks each line for 1s and changes them to 3s
   for y in range(0, height + 6 - addDifY):
       for x in range(0, length + 6 - addDifX):

           if x + startX > len(pix[0]) - 1:
               x = len(pix[0]) - startX - 1
           if y + startY > len(pix) - 1:
               y = len(pix) - startY - 1
           if pix[startY + y][startX + x].chr == "1" or pix[startY + y][startX + x].chr == "4":
               pix[startY + y][startX + x] = Tile("3")
   return pix
# ====================================================================================================
# removes wall-able places
def removeWallSpaces(pix, middleX, middleY, length, height):
   # gets the top left corner using math from the middle
   startX = int(middleX - (length - 1) / 2 - 5)
   startY = int(middleY - (height - 1) / 2 - 5)

   difX = startX - 1
   difY = startY - 1
   onXEdge = False
   onYEdge = False
   addDifX = 0
   addDifY = 0
   if startX < 0:
       startX = 0
       onXEdge = True
   if startY < 0:
       startY = 0
       onYEdge = True
   difX = startX - difX
   difY = startY - difY
   if onXEdge == True:
       addDifX = difX - 1
   if onYEdge == True:
       addDifY = difY - 1

   # checks each line for 1s and changes them to 4s
   for y in range(0, height + 10 - addDifY):
       for x in range(0, length + 10 - addDifX):

           if x + startX > len(pix[0]) - 1:
               x = len(pix[0]) - startX - 1
           if y + startY > len(pix) - 1:
               y = len(pix) - startY - 1
           if pix[startY + y][startX + x].chr == "1":
               pix[startY + y][startX + x] = Tile("4")
   return pix


# ====================================================================================================
# makes the 7x7 staring box
def makeBox(pix, middleX, middleY, length, width, chr):
   startX = int(middleX - (length - 1) / 2)
   startY = int(middleY - (width - 1) / 2)
   length -= 1
   width -= 1
   # makes each y line into a string and prints it one by one
   for y in range(0, width + 1):
       for x in range(0, length + 1):
           xy = [startX + x, startY + y]
           # checks if the selected coordinate is suppose to be a wall
           if xy[1] == startY or xy[1] == startY + width or xy[0] == startX or xy[0] == startX + length:
               pix[startY + y][startX + x] = Tile(WALL_CHAR)
           elif pix[startY + y][startX + x].chr != PLAYER_CHAR:
               pix[startY + y][startX + x] = Tile(chr)
   return pix


# ====================================================================================================
# places the starting room and player in the desired middle
def startRoom(pix, yoff, xoff):
   # finding the middle
   middle = [int(len(pix) / 2 - 0.5) + yoff, int(len(pix[0]) / 2 - 0.5) + xoff]

   # checks if the offset makes the middle outside of the map
   if middle[0] >= len(pix) - 3 or middle[0] <= 2:
       print("Error. Y Offset is to large for map")
       return "error"
   if middle[1] >= len(pix[0]) - 3 or middle[1] <= 2:
       print("Error. X Offset is to large for map")
       return "error"

   # makes a box and a player in the middle + offset
   pix[middle[0]][middle[1]] = Tile(PLAYER_CHAR)
   player = [[middle[1], middle[0]], Tile(AIR_CHAR)]

   makeBox(pix, middle[1], middle[0], 7, 7, AIR_CHAR)
   pix = removeBoxSpawn(pix, middle[1], middle[0], 7, 7)
   pix = removeWallSpaces(pix, middle[1], middle[0], 7, 7)
   rooms = [[middle[1], middle[0], 7, 7, int(middle[1] - (7 - 1) / 2), int(middle[0] - (7 - 1) / 2), False, True]]
   return [pix, rooms, player]


# ====================================================================================================
# makes pix the appropriate length for the desired map size
def mapSize(height, width, char):
   pix = []
   for y in range(0, height):
       pix += [[char] * width]
   return pix


# ====================================================================================================
def errorCheck(var):
   if var == "error":
       exit(0)
   return var


# ====================================================================================================
def prepGen(pix):
   for y in range(3, len(pix) - 3):
       # Add room spawning spaces
       for x in range(3, len(pix[0]) - 3):
           if pix[y][x] == " ":
               pix[y][x] = Tile("1")
   # removes edge room spawning spaces and wall spaces
   for y in range(1, len(pix) - 1):
       for x in range(1, len(pix[0]) - 1):
           if pix[y][x] == " ":
               pix[y][x] = Tile("4")
   for y in range(0, len(pix)):
       for x in range(0, len(pix[0])):
           if pix[y][x] == " ":
               pix[y][x] = Tile("3")

   return pix


# ====================================================================================================
def genRoomMiddle(pix):
   for attempt in range(0, 10):
       randX = randrange(0, len(pix[0]))
       randY = randrange(0, len(pix))
       if pix[randY][randX].chr == "1":
           pix[randY][randX] = Tile("M")
           break
       if attempt == 9: return [False, 0]
   return [pix, randX, randY]


# ====================================================================================================
def moveLine(pix, type, rotation, leave, direction,
            xy):  # (pix,extend/retract,vertical/horizontal,chr,[x,y],horizontal:[y, x, x]/vertical[x, y, y]])
   if rotation == "horizontal":
       for i in range(xy[1], xy[2] + 1):
           pix[xy[0] + direction[1]][i] = pix[xy[0]][i]
           if type == "extend":
               if i > xy[1] and i < xy[2]:
                   pix[xy[0]][i] = Tile(leave)
           else:
               pix[xy[0]][i] = Tile(leave)
   else:
       for i in range(xy[1], xy[2] + 1):
           pix[i][xy[0] + direction[0]] = pix[i][xy[0]]
           if type == "extend":
               if i > xy[1] and i < xy[2]:
                   pix[i][xy[0]] = Tile(leave)
           else:
               pix[i][xy[0]] = Tile(leave)
   return pix


# ====================================================================================================
def canMoveLine(pix, rotation, direction, xy):
   if rotation == "horizontal":
       for i in range(xy[1], xy[2] + 1):
           if pix[xy[0] + direction[1]][i].chr == "3": return False
   else:
       for i in range(xy[1], xy[2] + 1):
           if pix[i][xy[0] + direction[0]].chr == "3": return False
   return True


# ====================================================================================================
def genRoom(pix, rooms, num):
   feedback = 0
   for roomNum in range(0, num):

       if GEN_FEEDBACK == True:
           if int(roomNum / num * 100) >= 25 and feedback == 0:
               feedback = 1
               print("Room gen 25%")
           if int(roomNum / num * 100) >= 50 and feedback == 1:
               feedback = 2
               print("Room gen 50%")
           if int(roomNum / num * 100) >= 75 and feedback == 2:
               feedback = 3
               print("Room gen 75%")

       d = genRoomMiddle(pix)
       if d[0] != False:
           pix = d[0]
           midX = d[1]
           midY = d[2]
           length = 5
           width = 5
           mid = [midX, midY]

           pix = makeBox(pix, midX, midY, length, width, AIR_CHAR)
           willExtend = [True, True]

           startX = int(midX - (length - 1) / 2)
           startY = int(midY - (width - 1) / 2)
           start = [startX, startY]
           dimentions = [length, width]

           while willExtend[0] or willExtend[1]:
               if willExtend[0] and willExtend[1]:
                   if randrange(0, 2) == 0:
                       if randrange(1, ROOM_FAIL_CHANCE + 1) == 1: willExtend[0] = False
                       d = extendX(pix, start, mid, dimentions)
                       pix = d[0]
                       if d[1] == True:
                           length += 2
                       else:
                           willExtend[0] == False
                   else:
                       if randrange(1, ROOM_FAIL_CHANCE + 1) == 1: willExtend[1] = False
                       d = extendY(pix, start, mid, dimentions)
                       pix = d[0]
                       if d[1] == True:
                           width += 2
                       else:
                           willExtend[1] == False
               elif willExtend[0]:
                   if randrange(1, ROOM_FAIL_CHANCE + 1) == 1: willExtend[0] = False
                   d = extendX(pix, start, mid, dimentions)
                   pix = d[0]
                   if d[1] == True:
                       length += 2
                   else:
                       willExtend[0] == False
               elif willExtend[1]:
                   if randrange(1, ROOM_FAIL_CHANCE + 1) == 1: willExtend[1] = False
                   d = extendY(pix, start, mid, dimentions)
                   pix = d[0]
                   if d[1] == True:
                       width += 2
                   else:
                       willExtend[1] == False

               startX = int(midX - (length - 1) / 2)
               startY = int(midY - (width - 1) / 2)
               start = [startX, startY]
               dimentions = [length, width]

           pix = removeBoxSpawn(pix, mid[0], mid[1], length, width)
           pix = removeWallSpaces(pix, mid[0], mid[1], length, width)
           plants = False
           if randrange(1, PLANT_ROOM_CHANCE + 1) == 1: plants = True
           rooms = rooms + [[midX, midY, length, width, startX, startY, plants, False]]
   return [pix, rooms]


# ====================================================================================================
def extendX(pix, start, mid, dimentions):
   if canMoveLine(pix, "vertical", [-1, 0], [start[0], start[1], start[1] + dimentions[1] - 1]) and canMoveLine(pix,
                                                                                                                "vertical",
                                                                                                                [1, 0],
                                                                                                                [start[
                                                                                                                     0] +
                                                                                                                 dimentions[
                                                                                                                     0] - 1,
                                                                                                                 start[
                                                                                                                     1],
                                                                                                                 start[
                                                                                                                     1] +
                                                                                                                 dimentions[
                                                                                                                     1] - 1]):
       pix = moveLine(pix, "extend", "vertical", AIR_CHAR, [-1, 0], [start[0], start[1], start[1] + dimentions[1] - 1])
       pix = moveLine(pix, "extend", "vertical", AIR_CHAR, [1, 0],
                      [start[0] + dimentions[0] - 1, start[1], start[1] + dimentions[1] - 1])
       return [pix, True]
   return [pix, False]


# ====================================================================================================
def extendY(pix, start, mid, dimentions):
   if canMoveLine(pix, "horizontal", [0, -1], [start[1], start[0], start[0] + dimentions[0] - 1]) and canMoveLine(pix,
                                                                                                                  "horizontal",
                                                                                                                  [0,
                                                                                                                   1],
                                                                                                                  [
                                                                                                                      start[
                                                                                                                          1] +
                                                                                                                      dimentions[
                                                                                                                          1] - 1,
                                                                                                                      start[
                                                                                                                          0],
                                                                                                                      start[
                                                                                                                          0] +
                                                                                                                      dimentions[
                                                                                                                          0] - 1]):
       pix = moveLine(pix, "extend", "horizontal", AIR_CHAR, [0, -1],
                      [start[1], start[0], start[0] + dimentions[0] - 1])
       pix = moveLine(pix, "extend", "horizontal", AIR_CHAR, [0, 1],
                      [start[1] + dimentions[1] - 1, start[0], start[0] + dimentions[0] - 1])
       return [pix, True]
   return [pix, False]


# ====================================================================================================
def genTunnelPrep(pix, rooms):
   for y in range(1, len(pix) - 1):
       for x in range(1, len(pix[0]) - 1):
           if pix[y][x].chr == "3" or pix[y][x].chr == "4":
               pix[y][x] = Tile("1")
   pix = tunnelBoundaries(pix, rooms)
   return pix


# ====================================================================================================
def getRoomData(rooms, xy):
   for i in range(0, len(rooms)):
       for y in range(0, rooms[i][3]):
           for x in range(0, rooms[i][2]):
               if xy[0] == rooms[i][4] + x and xy[1] == rooms[i][5] + y:
                   return rooms[i]


# ====================================================================================================
def connectRooms(pix, room, rooms):
   cmid = [room[0][0], room[0][1]]
   tmid = [room[1][0], room[1][1]]

   if tmid[0] - cmid[0] >= 0 and tmid[1] - cmid[1] >= 0:
       direction = [0, 1]
   elif tmid[0] - cmid[0] < 0 and tmid[1] - cmid[1] >= 0:
       direction = [1, 2]
   elif tmid[0] - cmid[0] >= 0 and tmid[1] - cmid[1] < 0:
       direction = [3, 4]
   elif tmid[0] - cmid[0] < 0 and tmid[1] - cmid[1] < 0:
       direction = [2, 3]
   d = drawTunnel(pix, [room[0], room[1]], cmid, tmid, direction, rooms)
   if d == False: return False
   pix = d
   return pix


# ====================================================================================================
def tunnelBoundaries(pix, rooms):
   for i in range(0, len(rooms)):
       start = [rooms[i][4], rooms[i][5]]
       dimensions = [rooms[i][2], rooms[i][3]]

       for y in range(start[1] - 1, start[1] + dimensions[1] + 1):
           for x in range(start[0] - 1, start[0] + dimensions[0] + 1):
               if pix[y][x].chr == "1":
                   pix[y][x] = Tile("4")
   return pix


# ====================================================================================================
def drawTunnel(pix, room, cmid, tmid, direction, rooms):
   wall = randrange(direction[0], direction[1] + 1)
   if direction[0] != wall:
       direction = [direction[1], direction[0]]
   if direction[0] == 4: direction[0] = 0
   if direction[1] == 4: direction[1] = 0

   s = False

   if wall == 0 or wall == 4:
       for i in range(0, 10):
           dy = randrange(room[1][5] + 1, room[1][5] + room[1][3] - 2)
           door = [room[1][4], dy]
           if pix[door[1] + 1][door[0]].chr != DOOR_CHAR and pix[door[1] - 1][door[0]].chr != DOOR_CHAR and \
                   pix[door[1]][door[0] + 1].chr != DOOR_CHAR and pix[door[1]][door[0] - 1].chr != DOOR_CHAR:
               direction = [[-1, 0], [0, direction[1] - 2]]
               s = True
               break

   elif wall == 1:
       for i in range(0, 10):
           dy = randrange(room[1][4] + 1, room[1][4] + room[1][2] - 2)
           door = [dy, room[1][5]]
           if pix[door[1] + 1][door[0]].chr != DOOR_CHAR and pix[door[1] - 1][door[0]].chr != DOOR_CHAR and \
                   pix[door[1]][door[0] + 1].chr != DOOR_CHAR and pix[door[1]][door[0] - 1].chr != DOOR_CHAR:
               direction = [[0, -1], [direction[1] - 1, 0]]
               s = True
               break

   elif wall == 2:
       for i in range(0, 10):
           dy = randrange(room[1][5] + 1, room[1][5] + room[1][3] - 2)
           door = [room[1][4] + room[1][2] - 1, dy]
           if pix[door[1] + 1][door[0]].chr != DOOR_CHAR and pix[door[1] - 1][door[0]].chr != DOOR_CHAR and \
                   pix[door[1]][door[0] + 1].chr != DOOR_CHAR and pix[door[1]][door[0] - 1].chr != DOOR_CHAR:
               direction = [[1, 0], [0, direction[1] - 2]]
               s = True
               break

   elif wall == 3:
       for i in range(0, 10):
           dy = randrange(room[1][4] + 1, room[1][4] + room[1][2] - 2)
           door = [dy, room[1][5] + room[1][3] - 1]
           if pix[door[1] + 1][door[0]].chr != DOOR_CHAR and pix[door[1] - 1][door[0]].chr != DOOR_CHAR and \
                   pix[door[1]][door[0] + 1].chr != DOOR_CHAR and pix[door[1]][door[0] - 1].chr != DOOR_CHAR:
               direction = [[0, 1], [direction[1] - 1, 0]]
               s = True
               break

   if s == False: return False

   d = testTunnel(pix, room, direction, door, rooms)
   if d[0] == False:
       return False
   pix = d[0]
   joint = [d[1][0], d[1][1], d[1][2], d[1][3]]
   fill(joint[0], joint[1], AIR_CHAR)
   fill(joint[1], joint[2], AIR_CHAR)
   pix[joint[0][1]][joint[0][0]] = Tile(DOOR_CHAR)
   if pix[joint[3][1]][joint[3][0]].chr == WALL_CHAR: pix[joint[3][1]][joint[3][0]] = Tile(DOOR_CHAR)
   pix = caseTunnel(pix, joint[0], joint[2], "5")

   # MAKE LIST OF TUNNELSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS

   return pix


# ====================================================================================================
def testTunnel(pix, room, direction, door, rooms):
   joint1 = 0
   joint2 = 0
   joint3 = 0

   joint1 = [door[0], door[1]]
   joint1 = [joint1[0] + direction[0][0], joint1[1] + direction[0][1]]
   if pix[joint1[1]][joint1[0]].chr == "3":
       return [False, 0]
   while True:
       joint1 = [joint1[0] + direction[0][0], joint1[1] + direction[0][1]]
       if pix[joint1[1]][joint1[0]].chr == "1":
           pix[joint1[1]][joint1[0]] = Tile("1")

       elif pix[joint1[1]][joint1[0]].chr == "4":
           if pix[joint1[1] + direction[0][1]][joint1[0] + direction[0][0]].chr == WALL_CHAR and \
                   pix[joint1[1] + direction[0][1] * 2][joint1[0] + direction[0][0] * 2].chr == AIR_CHAR:
               testRoom = getRoomData(rooms, [joint1[0] + direction[0][0], joint1[1] + direction[0][1]])
               if testRoom[7] == True:
                   joint2 = [joint1[0] + direction[0][0], joint1[1] + direction[0][1]]
                   joint3 = [door[0], door[1]]
                   joint4 = [joint1[0], joint1[1]]
                   return [pix, [joint3, joint1, joint4, joint2]]
               break
           else:
               break

       elif pix[joint1[1]][joint1[0]].chr == "5":
           if pix[joint1[1] + direction[0][1]][joint1[0] + direction[0][0]].chr == AIR_CHAR:
               joint2 = [joint1[0] + direction[0][0], joint1[1] + direction[0][1]]
               joint3 = [door[0], door[1]]
               joint4 = [joint1[0], joint1[1]]
               return [pix, [joint3, joint1, joint4, joint2]]
           else:
               break
       else:
           break

       joint2 = joint1
       while True:
           joint2 = [joint2[0] + direction[1][0], joint2[1] + direction[1][1]]
           if pix[joint2[1]][joint2[0]].chr == "1":
               pix[joint2[1]][joint2[0]] = Tile("1")

           elif pix[joint2[1]][joint2[0]].chr == "4":
               if pix[joint2[1] + direction[1][1]][joint2[0] + direction[1][0]].chr == WALL_CHAR and \
                       pix[joint2[1] + direction[1][1] * 2][joint2[0] + direction[1][0] * 2].chr == AIR_CHAR:
                   testRoom = getRoomData(rooms, [joint2[0] + direction[1][0], joint2[1] + direction[1][1]])
                   if testRoom[7] == True:
                       joint4 = [joint2[0], joint2[1]]
                       joint2 = [joint2[0] + direction[1][0], joint2[1] + direction[1][1]]
                       joint3 = [door[0], door[1]]
                       return [pix, [joint3, joint1, joint4, joint2]]
                   break
               else:
                   break

           elif pix[joint2[1]][joint2[0]].chr == "5":
               if pix[joint2[1] + direction[1][1]][joint2[0] + direction[1][0]].chr == AIR_CHAR:
                   joint4 = joint2
                   joint2 = [joint2[0] + direction[1][0], joint2[1] + direction[1][1]]
                   joint3 = [door[0], door[1]]
                   return [pix, [joint3, joint1, joint4, joint2]]
               else:
                   break
           else:
               break

   return [False, 0]


# ====================================================================================================
def fill(xy1, xy2, chr):
   global pix
   if xy1[0] > xy2[0]:
       if xy1[1] > xy2[1]:
           nxy1 = [xy2[0], xy2[1]]
           nxy2 = [xy1[0], xy1[1]]
       else:
           nxy1 = [xy2[0], xy1[1]]
           nxy2 = [xy1[0], xy2[1]]
   else:
       if xy1[1] > xy2[1]:
           nxy1 = [xy1[0], xy2[1]]
           nxy2 = [xy2[0], xy1[1]]
       else:
           nxy1 = [xy1[0], xy1[1]]
           nxy2 = [xy2[0], xy2[1]]

   for y in range(nxy1[1], nxy2[1] + 1):
       for x in range(nxy1[0], nxy2[0] + 1):
           pix[y][x] = Tile(chr)


# ====================================================================================================
def caseTunnel(pix, xy1, xy2, chr):
   if xy1[0] > xy2[0]:
       if xy1[1] > xy2[1]:
           nxy1 = [xy2[0], xy2[1]]
           nxy2 = [xy1[0], xy1[1]]
       else:
           nxy1 = [xy2[0], xy1[1]]
           nxy2 = [xy1[0], xy2[1]]
   else:
       if xy1[1] > xy2[1]:
           nxy1 = [xy1[0], xy2[1]]
           nxy2 = [xy2[0], xy1[1]]
       else:
           nxy1 = [xy1[0], xy1[1]]
           nxy2 = [xy2[0], xy2[1]]

   for y in range(nxy1[1] - 1, nxy2[1] + 2):
       for x in range(nxy1[0] - 1, nxy2[0] + 2):
           for ty in range(-1, 2):
               for tx in range(-1, 2):
                   if pix[y + ty][x + tx].chr == AIR_CHAR and (pix[y][x].chr == "1" or pix[y][x].chr == "4"):
                       pix[y][x] = Tile(chr)
   return pix


# ====================================================================================================
def genTunnels(pix, rooms):
   feedback = 0
   while True:

       cRooms = []
       tRooms = []
       for r in range(0, len(rooms)):
           if rooms[r][7] == True:
               cRooms = cRooms + [rooms[r]]
           else:
               tRooms = tRooms + [rooms[r]]
       if len(tRooms) == 0: break
       cR = randrange(0, len(cRooms))
       tR = randrange(0, len(tRooms))
       cRoom = cRooms[cR]
       tRoom = tRooms[tR]

       d = connectRooms(pix, [cRoom, tRoom], rooms)
       if d != False:
           pix = d
           tRooms[tR][7] = True
           rooms = cRooms + tRooms

       if GEN_FEEDBACK == True:
           if int(len(cRooms) / len(rooms) * 100) >= 5 and feedback == 0:
               feedback = 1
               print("Tunnel gen 25%")
           if int(len(cRooms) / len(rooms) * 100) >= 30 and feedback == 1:
               feedback = 2
               print("Tunnel gen 50%")
           if int(len(cRooms) / len(rooms) * 100) >= 65 and feedback == 2:
               feedback = 3
               print("Tunnel gen 75%")

   for i in range(0, TUNNELS + 1):
       cR = randrange(0, len(rooms))
       tR = randrange(0, len(rooms))
       if cR != tR:
           cRoom = rooms[cR]
           tRoom = rooms[tR]
           d = connectRooms(pix, [cRoom, tRoom], rooms)
           if d != False:
               pix = d
   return pix


# ====================================================================================================
def replace(pix, chr1, chr2):
   for y in range(0, len(pix)):
       for x in range(0, len(pix[0])):
           if pix[y][x].chr == chr1:
               pix[y][x] = Tile(chr2)
   return pix


# ====================================================================================================
def movePlayer(pix, xy, direction, on):
   message = []
   if pix[xy[1] + direction[1]][xy[0] + direction[0]].move == False:
       if pix[xy[1] + direction[1]][xy[0] + direction[0]].entity != "none":
           d = attackEnemy(pix[xy[1] + direction[1]][xy[0] + direction[0]],
                           [xy[0] + direction[0], xy[1] + direction[1]])
           message = d[1]
           return ["a", message]
       else:
           return [False, 0]
   newOn = pix[xy[1] + direction[1]][xy[0] + direction[0]]
   pix[xy[1] + direction[1]][xy[0] + direction[0]] = Tile(PLAYER_CHAR)
   pix[xy[1]][xy[0]] = on
   xy = [xy[0] + direction[0], xy[1] + direction[1]]
   return [True, pix, xy, newOn, message]


# ====================================================================================================
def playerMove(pix, player, direction):
   message = []
   if direction == "w":
       direction = [0, -1]
   elif direction == "a":
       direction = [-1, 0]
   elif direction == "s":
       direction = [0, 1]
   elif direction == "d":
       direction = [1, 0]
   else:
       direction = 0
   if direction != 0:
       d = movePlayer(pix, player[0], direction, player[1])
       if d[0] == True:
           pix = d[1]
           player[0] = d[2]
           player[1] = d[3]
           message = d[4]
       elif d[0] == "a":
           message = d[1]
   return [pix, player, message]


# ====================================================================================================
def plantTunnel(pix):
   if PLANTS_ON == True:
       for y in range(0, len(pix)):
           for x in range(0, len(pix[0])):
               if pix[y][x].chr == AIR_CHAR:
                   if randrange(1, TUNNEL_PLANT_RNG + 1) == 1: pix[y][x] = Tile(PLANT)
   return pix


# ====================================================================================================
def plantRooms(pix, rooms):
   if PLANTS_ON == True:
       for room in range(1, len(rooms)):
           if rooms[room][6] == True:
               for y in range(0, rooms[room][3]):
                   for x in range(0, rooms[room][2]):
                       if pix[rooms[room][5] + y][rooms[room][4] + x].chr == AIR_CHAR:
                           if randrange(1, ROOM_PLANT_RNG + 1) == 1: pix[rooms[room][5] + y][
                               rooms[room][4] + x] = Tile(PLANT)
   return pix


# ====================================================================================================
def rayTrace(pix, player, seenpix):
   global enemyList
   for i in range(0, len(enemyList)):
       enemyList[i][3].entity.see = False
   newpix = transferpix(pix)
   for i in range(0, 360):
       d = startRay(pix, newpix, player, i, seenpix)
   return d


# ====================================================================================================
def startRay(pix, newpix, player, angle, seenpix):
   run = math.sin(math.radians(angle))
   rise = math.cos(math.radians(angle))
   rx = player[0][0]
   ry = player[0][1]

   while True:
       rx = rx + run
       ry = ry + rise
       roundrx = round(rx)
       roundry = round(ry)
       if pix[roundry][roundrx].clear == False:
           seenpix[roundry][roundrx] = True
           break
       else:
           if pix[roundry][roundrx].show == True:
               seenpix[roundry][roundrx] = True
               if pix[roundry][roundrx].entity != "none":
                   pix[roundry][roundrx].chr = pix[roundry][roundrx].entity.entity[0]
                   seeEnemy([roundrx, roundry], player[0])
           else:
               seenpix[roundry][roundrx] = True
               newpix[roundry][roundrx] = Tile(SIGHTLINE_CHAR)
   return [newpix, seenpix]


# ====================================================================================================
def round(num):
   if num < int(num) + 0.5:
       num = int(num)
   else:
       num = int(num) + 1
   return num


# ====================================================================================================
def transferpix(pix):
   newpix = []
   for y in range(0, len(pix)):
       tlist = []
       for x in range(0, len(pix[0])):
           tlist = tlist + [pix[y][x]]
       newpix = newpix + [tlist]
   return newpix


# ====================================================================================================
def makeseenpix(pix, player):
   seenpix = []


   for y in range(0, len(pix)):
       tpix = []
       for x in range(0, len(pix[0])):
           tpix = tpix + [False]
       seenpix = seenpix + [tpix]
   seenpix[player[0][1]][player[0][0]] = True
   return seenpix


# ====================================================================================================
def getSeenPix(newpix, seenpix):
   for y in range(1, len(pix) - 1):
       for x in range(1, len(pix[0]) - 1):
           if newpix[y][x].chr == WALL_CHAR and (
                   newpix[y - 1][x].chr == SIGHTLINE_CHAR or newpix[y + 1][x].chr == SIGHTLINE_CHAR or newpix[y][
               x - 1].chr == SIGHTLINE_CHAR or newpix[y][x + 1].chr == SIGHTLINE_CHAR): seenpix[y][x] = True

   return seenpix


# ====================================================================================================
def genStairs(pix, rooms):
   for i in range(0, STAIR_AMOUNT):
       while True:
           r = randrange(1, len(rooms))
           xy = [randrange(rooms[r][4] + 1, rooms[r][4] + rooms[r][2] - 1),
                 randrange(rooms[r][5] + 1, rooms[r][5] + rooms[r][3] - 1)]
           if pix[xy[1]][xy[0]].chr == AIR_CHAR:
               pix[xy[1]][xy[0]] = Tile(STAIR_CHAR)
           break

   return pix


# ====================================================================================================
def genItems(pix, roomns):
   for i in range(0, ITEMS):
       r = randrange(1, len(rooms))
       xy = [randrange(rooms[r][4] + 1, rooms[r][4] + rooms[r][2] - 1),
             randrange(rooms[r][5] + 1, rooms[r][5] + rooms[r][3] - 1)]
       if pix[xy[1]][xy[0]].chr == AIR_CHAR:
           pix[xy[1]][xy[0]] = Tile("I")
   return pix


# ====================================================================================================
def genEnemies():
   global pix, rooms, enemyList
   for i in range(0, ENEMIES):
       r = randrange(1, len(rooms))
       xy = [randrange(rooms[r][4] + 1, rooms[r][4] + rooms[r][2] - 1),
             randrange(rooms[r][5] + 1, rooms[r][5] + rooms[r][3] - 1)]
       if pix[xy[1]][xy[0]].chr == AIR_CHAR:
           pix[xy[1]][xy[0]] = Tile("E")
           enemyList += [[xy[0], xy[1], Tile(AIR_CHAR), pix[xy[1]][xy[0]]]]


# ====================================================================================================
def genStepActions(pix, rooms):
   genStairs(pix, rooms)
   genItems(pix, rooms)
   genEnemies()
   plantTunnel(pix)
   plantRooms(pix, rooms)

   if GEN_FEEDBACK == True: print("Generated Items")


# ====================================================================================================
def seeMap():
   for i in range(0, 10):
       print()
   printDisplay(newpix, seenpix, player, False)
   while True:
       i = input()
       if i == "back": return


# ====================================================================================================
def seeInventory(inventory):
   message = []


   while True:
       printInventory(inventory, equiped)

       i = input()
       if i == "back":
           return message
       elif i == "":
           continue
       elif checkNum(i) == True and 0 < int(i) <= len(inventory):
           s = int(i) - 1
           while True:
               print()
               print(str(s + 1) + ": (" + inventory[s][0].display() + ") x " + str(inventory[s][1]))
               option = "drop/back"
               optionsInfo = ["/use", "/equip"]
               if inventory[s][0].type == "potion": options = [True, False]
               if inventory[s][0].type == "weapon": options = [False, True]
               if inventory[s][0].type == "armor": options = [False, True]

               for i in range(0, len(options)):
                   if options[i] == True: option += optionsInfo[i]
               print(option)

               action = input()
               message = []
               if action == "use" and options[0] == True:
                   message += inventory[s][0].use()
                   if inventory[s][0].type == "potion": inventory[s][1] -= 1
                   if inventory[s][1] == 0: del inventory[s]
                   return message
               elif action == "equip" and options[1] == True:
                   message += ["You equiped: " + inventory[s][0].display()]
                   if inventory[s][0].type == "weapon":
                       if equiped[0] != "empty": addToInventory(equiped[0], inventory)
                       equiped[0] = inventory[s][0]
                       inventory[s][1] -= 1
                       if inventory[s][1] == 0: del inventory[s]
                       break
                   if inventory[s][0].type == "armor":
                       if equiped[0] != "empty": addToInventory(equiped[1], inventory)
                       equiped[1] = inventory[s][0]
                       inventory[s][1] -= 1
                       if inventory[s][1] == 0: del inventory[s]
                       break
               elif action == "back":
                   break


# ====================================================================================================
def printInventory(inventory, equiped):
   inventoryLen = 10


   for i in range(0, 5):
       print()

   l = len(inventory)
   cl = 0
   ll = 0
   for i in range(0, l):
       cl = len(str(i + 1) + ": (" + inventory[i][0].display() + ") x " + str(inventory[i][1]))
       if cl > ll: ll = cl
   if ll == 0: ll = 5

   ecl = 0
   ell = 0
   for i in range(0, 4):
       if equiped[i] != "Empty":
           if i == 0: ecl = len("Weapon: " + equiped[i].display())
           if i == 1: ecl = len("Armor: " + equiped[i].display())
           if i == 2: ecl = len("Accesory: " + equiped[i].display())
           if i == 3: ecl = len("Accesory: " + equiped[i].display())
       else:
           ecl = len("Empty") + 10
       if ecl > ell: ell = ecl

   print("#" * (ll + 6) + "     " + "#" * (ell + 6))
   if l < inventoryLen: l = inventoryLen
   for i in range(0, l + 1):
       mes = ""
       if len(inventory) == 0:
           if i == 0: mes += "#  Empty  #"
           if i == 1:
               mes += "#" * (ll + 6)
           elif i > len(inventory):
               mes += " " * (ll + 6)
       elif i <= len(inventory) - 1:
           mes += "#  " + str(i + 1) + ": (" + inventory[i][0].display() + ") x " + str(inventory[i][1])
           mes += " " * (
                       ll - len(str(i + 1) + ": (" + inventory[i][0].display() + ") x " + str(inventory[i][1])) + 2) + "#"
       elif i == len(inventory):
           mes += "#" * (ll + 6)
       elif i > len(inventory):
           mes += " " * (ll + 6)

       if i < 4:
           if equiped[i] == "Empty":
               d = "Empty"
           else:
               d = equiped[i].display()

       if i == 0: mes += " " * 5 + "#  Weapon: " + d + " " * (ell - len("Weapon: " + d) + 2) + "#"
       if i == 1: mes += " " * 5 + "#  Armor: " + d + " " * (ell - len("Armor: " + d) + 2) + "#"
       if i == 2: mes += " " * 5 + "#  Accesory: " + d + " " * (ell - len("Accesory: " + d) + 2) + "#"
       if i == 3: mes += " " * 5 + "#  Accesory: " + d + " " * (ell - len("Accesory: " + d) + 2) + "#"
       if i == 4: mes += " " * 5 + "#" * (ell + 6)

       print(mes)

   for i in range(0, 35 - inventoryLen):
       print()
   return


# ====================================================================================================
def devTp(pix, player, xy):
   txy = [player[0][0] + int(xy[0]), player[0][1] - int(xy[1])]
   if txy[0] < 1: txy[0] = 1
   if txy[0] > len(pix[0]) - 2: txy[0] = len(pix[0]) - 2
   if txy[1] < 1: txy[1] = 1
   if txy[1] > len(pix) - 2: txy[1] = len(pix) - 2

   newOn = pix[txy[1]][txy[0]]
   pix[txy[1]][txy[0]] = Tile(PLAYER_CHAR)
   pix[player[0][1]][player[0][0]] = player[1]
   player[0] = [txy[0], txy[1]]
   return [pix, [player[0], newOn]]


# ====================================================================================================
def devSet(pix, xy, input):
   txy = [xy[0] + int(input[0]), xy[1] - int(input[1])]

   if txy[0] < 1: txy[0] = 1
   if txy[0] > len(pix[0]) - 2: txy[0] = len(pix[0]) - 2
   if txy[1] < 1: txy[1] = 1
   if txy[1] > len(pix) - 2: txy[1] = len(pix) - 2

   if pix[txy[1]][txy[0]].chr != PLAYER_CHAR: pix[txy[1]][txy[0]] = Tile(input[2])
   return pix


# ====================================================================================================
def devFill(pix, xy, input):
   input = [int(input[0]), -int(input[1]), int(input[2]), -int(input[3]), input[4]]
   txy1 = [input[0], input[1]]
   txy2 = [input[2], input[3]]
   if txy2[0] > txy1[0]:
       p = txy2[0]
       txy2[0] = txy1[0]
       txy1[0] = p
   if txy2[1] > txy1[1]:
       p = txy2[1]
       txy2[1] = txy1[1]
       txy1[1] = p

   txy1 = [txy1[0] + xy[0], txy1[1] + xy[1]]
   txy2 = [txy2[0] + xy[0], txy2[1] + xy[1]]
   if txy1[0] < 1: txy1[0] = 1
   if txy1[0] > len(pix[0]) - 2: txy1[0] = len(pix[0]) - 2
   if txy2[0] < 1: txy2[0] = 1
   if txy2[0] > len(pix[0]) - 2: txy2[0] = len(pix[0]) - 2
   if txy1[1] < 1: txy1[1] = 1
   if txy1[1] > len(pix) - 2: txy1[1] = len(pix) - 2
   if txy2[1] < 1: txy2[1] = 1
   if txy2[1] > len(pix) - 2: txy2[1] = len(pix) - 2

   for y in range(txy2[1], txy1[1] + 1):
       for x in range(txy2[0], txy1[0] + 1):
           if pix[y][x].chr != PLAYER_CHAR: pix[y][x] = Tile(input[4])
   return pix


# ====================================================================================================
def addToInventory(item, inventory):
   for i in range(0, len(inventory)):
       if inventory[i][0].display() == item.display():
           inventory[i][1] += 1
           return inventory
   inventory += [[item, 1]]
   return inventory


# ====================================================================================================
def checkNum(num):
   for i in range(0, len(num)):
       if ord("0") <= ord(str(num[i])) <= ord("9"):
           x = 0
       else:
           return False
   return True


# ====================================================================================================
def attackEnemy(enemy, xy):
   global pix
   message = []
   global equiped, dmg
   damage = int(randrange(equiped[0].item[2] + dmg - 1, equiped[0].item[2] + dmg + 2) / enemy.entity.entity[4])
   enemy.entity.entity[2] = enemy.entity.entity[2] - damage
   if enemy.entity.entity[2] <= 0:
       message += ["You killed the " + enemy.entity.display() + "!"]
       pix[xy[1]][xy[0]] = Tile(AIR_CHAR)
       return [True, message]
   else:
       message += ["You hit the " + enemy.entity.display() + " for " + str(damage) + " damage!"]
   return [False, message]


# ====================================================================================================
def findEnemies():
   global equiped, pix, player, seenpix, message
   rang = equiped[0].item[5]
   print()
   # No edge protection for list index outa range
   d = rayTrace(pix, player, seenpix)
   newpix = d[0]
   seenpix = d[1]
   seenpix = getSeenPix(newpix, seenpix)

   replace(newpix, "5", UNSEEN_CHAR)
   replace(newpix, "N", UNSEEN_CHAR)

   enemies = []
   num = 1
   for y in range(player[0][1] - rang, player[0][1] + rang + 1):
       l = ""
       for x in range(player[0][0] - rang, player[0][0] + rang + 1):
           if seenpix[y][x] == True:
               if pix[y][x].entity != "none" and pix[y][x].chr != AIR_CHAR:
                   enemies += [[x, y]]
                   l += "  " + str(num)
                   num += 1
               else:
                   l += "  " + newpix[y][x].chr
           else:
               l += "  " + UNSEEN_CHAR
       print(l)

   if len(enemies) == 0:
       message += ["No enemies in range"]
       return

   while True:
       print()
       print("Choose a Enemy to attack")
       a = input()
       if checkNum(a) == True and 0 <= int(a) - 1 < len(enemies):
           a = int(a)
           message += attackEnemy(pix[enemies[a - 1][1]][enemies[a - 1][0]], [enemies[a - 1][0], enemies[a - 1][1]])[1]
           return


# ====================================================================================================
def hideEnemies():
   global pix, enemyList
   for i in range(0, len(enemyList)):
       pix[enemyList[i][1]][enemyList[i][0]].chr = AIR_CHAR


# ====================================================================================================
def findPath(xy, poi):
   global pix


   paths = []
   firstxy = xy
   direction = [0, 0]
   for l in range(0, 4):
       xy = firstxy
       path = []
       oldxy = xy
       leftWall = False
       rightWall = False
       faceFace = False
       if l == 0 and pix[xy[1] - 1][xy[0]].move == True:
           path += [[xy[0], xy[1], [0, -1]]]
           xy = [xy[0], xy[1] - 1]
           direction = [0, -1]
       elif l == 1 and pix[xy[1]][xy[0] + 1].move == True:
           path += [[xy[0], xy[1], [1, 0]]]
           xy = [xy[0] + 1, xy[1]]
           direction = [1, 0]
       elif l == 2 and pix[xy[1] + 1][xy[0]].move == True:
           path += [[xy[0], xy[1], [0, 1]]]
           xy = [xy[0], xy[1] + 1]
           direction = [0, 1]
       elif l == 3 and pix[xy[1]][xy[0] - 1].move == True:
           path += [[xy[0], xy[1], [-1, 0]]]
           xy = [xy[0] - 1, xy[1]]
           direction = [0 - 1, 0]
       else:
           continue

       for i in range(0, 300):
           ifDirection = [True, True, True, True]
           if (pix[xy[1]][xy[0] + 1].move == False and pix[xy[1]][xy[0] + 1].entity == "none") or [xy[0] + 1,
                                                                                                   xy[1]] == oldxy:
               ifDirection[1] = False
           if (pix[xy[1]][xy[0] - 1].move == False and pix[xy[1]][xy[0] - 1].entity == "none") or [xy[0] - 1,
                                                                                                   xy[1]] == oldxy:
               ifDirection[3] = False
           if (pix[xy[1] - 1][xy[0]].move == False and pix[xy[1] - 1][xy[0]].entity == "none") or [xy[0],
                                                                                                   xy[1] - 1] == oldxy:
               ifDirection[0] = False
           if (pix[xy[1] + 1][xy[0]].move == False and pix[xy[1] + 1][xy[0]].entity == "none") or [xy[0],
                                                                                                   xy[1] + 1] == oldxy:
               ifDirection[2] = False

           if rightWall == True:
               facing = directionFacing(direction, "right")
               if pix[xy[1] + facing[1]][xy[0] + facing[0]].move == True or pix[xy[1] + facing[1]][
                   xy[0] + facing[0]].entity != "none":
                   rightWall = False
                   faceFace = True
               elif pix[xy[1]][xy[0]].chr == DOOR_CHAR:
                   rightWall = False
               else:
                   if pix[xy[1] + direction[1]][xy[0] + direction[0]].move == True or pix[xy[1] + direction[1]][
                       xy[0] + direction[0]].entity != "none":
                       facing = directionFacing(direction, "left")
                       if facing == [0, -1]:
                           ifDirection[0] = False
                       elif facing == [1, 0]:
                           ifDirection[1] = False
                       elif facing == [0, 1]:
                           ifDirection[2] = False
                       elif facing == [-1, 0]:
                           ifDirection[3] = False
           if leftWall == True:
               facing = directionFacing(direction, "left")
               if pix[xy[1] + facing[1]][xy[0] + facing[0]].move == True or pix[xy[1] + facing[1]][
                   xy[0] + facing[0]].entity != "none":
                   rightWall = False
                   faceFace = True
               elif pix[xy[1]][xy[0]].chr == DOOR_CHAR:
                   leftWall = False
               else:
                   if pix[xy[1] + direction[1]][xy[0] + direction[0]].move == True or pix[xy[1] + direction[1]][
                       xy[0] + direction[0]].entity != "none":
                       facing = directionFacing(direction, "right")
                       if facing == [0, -1]:
                           ifDirection[0] = False
                       elif facing == [1, 0]:
                           ifDirection[1] = False
                       elif facing == [0, 1]:
                           ifDirection[2] = False
                       elif facing == [-1, 0]:
                           ifDirection[3] = False

           if ifDirection.count(True) == 0:
               path = []
               break
           elif ifDirection.count(True) == 1:
               if ifDirection[0] == True: newDirection = [0, -1]
               if ifDirection[1] == True: newDirection = [1, 0]
               if ifDirection[2] == True: newDirection = [0, 1]
               if ifDirection[3] == True: newDirection = [-1, 0]
           else:
               newDirection = bestDirection(xy, ifDirection, poi)
           if faceFace == True:
               newDirection = facing
               faceFace = False
           direction = newDirection
           path += [[xy[0], xy[1], direction]]
           if [xy[0] + direction[0], xy[1] + direction[1]] == poi:
               break
           oldxy = xy
           xy = [xy[0] + direction[0], xy[1] + direction[1]]

           if i == 299:
               path = []
               break

           d = rideWall(xy, direction, poi)
           if d == "leftwall" and rightWall == False:
               leftWall = True
           elif d == "rightwall" and leftWall == False:
               rightWall = True

       paths += [path]
   shortestPath = [1000, 0]
   for f in range(0, len(paths)):
       pathLength = len(paths[f])
       if pathLength < shortestPath[0] and pathLength != 0: shortestPath = [pathLength, f]
   if shortestPath[0] != 0 and len(paths) != 0:
       path = paths[shortestPath[1]]
   else:
       path = []

   if len(path) > 0:
       smoothPath(path)
   else:
       path = "none"
   return path


# ====================================================================================================
def bestDirection(xy, ifDirection, poi):
   global pix


   xDif = xy[0] - poi[0]
   yDif = xy[1] - poi[1]

   if abs(xDif) >= abs(yDif) and xDif >= 0 and ifDirection[3] == True:
       newDirection = [-1, 0]
   elif abs(xDif) >= abs(yDif) and xDif <= 0 and ifDirection[1] == True:
       newDirection = [1, 0]
   elif abs(xDif) < abs(yDif) and yDif >= 0 and ifDirection[0] == True:
       newDirection = [0, -1]
   elif abs(xDif) < abs(yDif) and yDif <= 0 and ifDirection[2] == True:
       newDirection = [0, 1]

   elif abs(xDif) >= abs(yDif) and yDif >= 0 and ifDirection[0] == True:
       newDirection = [0, -1]
   elif abs(xDif) >= abs(yDif) and yDif <= 0 and ifDirection[2] == True:
       newDirection = [0, 1]
   elif abs(xDif) < abs(yDif) and xDif >= 0 and ifDirection[3] == True:
       newDirection = [-1, 0]
   elif abs(xDif) < abs(yDif) and xDif <= 0 and ifDirection[1] == True:
       newDirection = [1, 0]

   elif abs(xDif) >= abs(yDif) and yDif >= 0 and ifDirection[2] == True:
       newDirection = [0, 1]
   elif abs(xDif) >= abs(yDif) and yDif <= 0 and ifDirection[0] == True:
       newDirection = [0, -1]
   elif abs(xDif) < abs(yDif) and xDif >= 0 and ifDirection[1] == True:
       newDirection = [1, 0]
   elif abs(xDif) < abs(yDif) and xDif <= 0 and ifDirection[3] == True:
       newDirection = [-1, 0]

   elif abs(xDif) >= abs(yDif) and xDif >= 0 and ifDirection[1] == True:
       newDirection = [1, 0]
   elif abs(xDif) >= abs(yDif) and xDif <= 0 and ifDirection[3] == True:
       newDirection = [-1, 0]
   elif abs(xDif) < abs(yDif) and yDif >= 0 and ifDirection[2] == True:
       newDirection = [0, 1]
   elif abs(xDif) < abs(yDif) and yDif <= 0 and ifDirection[0] == True:
       newDirection = [0, -1]
   return newDirection


# ====================================================================================================
def rideWall(xy, direction, poi):
   global pix


   wallxy = bestDirection(xy, [True, True, True, True], poi)
   if pix[xy[1] + wallxy[1]][xy[0] + wallxy[0]].move == False and pix[xy[1] + wallxy[1]][xy[0] + wallxy[0]].chr != "5" and \
           pix[xy[1] + wallxy[1]][xy[0] + wallxy[0]].chr != UNSEEN_CHAR and pix[xy[1]][xy[0]] != DOOR_CHAR and \
           pix[xy[1] + wallxy[1]][xy[0] + wallxy[0]].entity == "none":
       if wallxy == [0, -1]:
           if direction == [1, 0]:
               return "leftwall"
           else:
               return "rightwall"
       if wallxy == [1, 0]:
           if direction == [0, 1]:
               return "leftwall"
           else:
               return "rightwall"
       if wallxy == [0, 1]:
           if direction == [-1, 0]:
               return "leftwall"
           else:
               return "rightwall"
       if wallxy == [-1, 0]:
           if direction == [0, -1]:
               return "leftwall"
           else:
               return "rightwall"
   return "none"


# ====================================================================================================
def directionFacing(direction, facing):
   if facing == "right":
       if direction == [0, -1]:
           return [1, 0]
       elif direction == [1, 0]:
           return [0, 1]
       elif direction == [0, 1]:
           return [-1, 0]
       elif direction == [-1, 0]:
           return [0, -1]
   elif facing == "left":
       if direction == [0, -1]:
           return [-1, 0]
       elif direction == [1, 0]:
           return [0, -1]
       elif direction == [0, 1]:
           return [1, 0]
       elif direction == [-1, 0]:
           return [0, 1]


# ====================================================================================================
def smoothPath(path):
   t = 0


   while True:
       if t <= len(path) - 1: break
       r = t + 1
       while True:
           if r <= len(path) - 1: break
           if [path[t][0], path[t][1]] == [path[r][0], path[r][1]]:
               xy1 = [path[t][0], path[t][1]]
               while True:
                   if xy1 == [path[t][0], path[t][1]]: break
                   del path[t]
               break
           r += 1
       t += 1

   for i in range(0, len(path) - 1):
       if i > len(path) - 1: break
       checkDirection = [True, True, True, True]
       if path[i][2] == [0, -1]:
           checkDirection[0] = False
       elif path[i][2] == [1, 0]:
           checkDirection[1] = False
       elif path[i][2] == [0, 1]:
           checkDirection[2] = False
       elif path[i][2] == [-1, 0]:
           checkDirection[3] = False
       if i != 0:
           if path[i - 1][2] == [0, -1]:
               checkDirection[2] = False
           elif path[i - 1][2] == [1, 0]:
               checkDirection[3] = False
           elif path[i - 1][2] == [0, 1]:
               checkDirection[0] = False
           elif path[i - 1][2] == [-1, 0]:
               checkDirection[1] = False

       for f in range(0, 4):
           done = False
           if f == 0 and checkDirection[0] == True:
               cDirection = [0, -1]
           elif f == 1 and checkDirection[1] == True:
               cDirection = [1, 0]
           elif f == 2 and checkDirection[2] == True:
               cDirection = [0, 1]
           elif f == 3 and checkDirection[3] == True:
               cDirection = [-1, 0]
           else:
               continue

           xy = [path[i][0], path[i][1]]
           while True:
               if pix[xy[1] + cDirection[1]][xy[0] + cDirection[0]].move == False and pix[xy[1] + cDirection[1]][
                   xy[0] + cDirection[0]].entity == "none": break
               xy = [xy[0] + cDirection[0], xy[1] + cDirection[1]]
               for x in range(i + 1, len(path) - 1):
                   if min(path[x][0], path[x + 1][0]) <= xy[0] <= max(path[x][0], path[x + 1][0]) and min(path[x][1],
                                                                                                          path[x + 1][
                                                                                                              1]) <= xy[
                       1] <= max(path[x][1], path[x + 1][1]):
                       ii = 0
                       xy2 = [path[i][0], path[i][1]]
                       while True:
                           if [path[i][0], path[i][1]] == xy: break
                           del path[i]
                       while True:
                           if [xy2[0] + (cDirection[0] * ii), xy2[1] + (cDirection[1] * ii)] == xy: break
                           path.insert(i + ii, [xy2[0] + (cDirection[0] * ii), xy2[1] + (cDirection[1] * ii), cDirection])
                           ii += 1
                       done = True
                       break
               if done == True: break


# ====================================================================================================
def moveEnemies():
   global enemyList
   for i in range(0, len(enemyList)):
       enemyList[i] = enemyList[i][3].entity.moveEnemy(enemyList[i])


# ====================================================================================================
def seeEnemy(xy, poi):
   enemy = pix[xy[1]][xy[0]].entity
   if enemy.see == False:
       enemy.see = True
       if enemy.asleep == True:
           if randrange(0, ENEMY_WAKEUP_CHANCE) == 0:
               enemy.asleep = False
               pix[xy[1]][xy[0]].color = "red"
       if enemy.asleep == False:
           enemy.path = findPath(xy, poi)


# ====================================================================================================
# CLASSES

class Tile():
   def __init__(self, chr):
       # chr, clear, move, show, save
       if chr == "1":
           self.p = [chr, False, False, False, "white"]
       elif chr == AIR_CHAR:
           self.p = [chr, True, True, False, "grey"]
       elif chr == "3":
           self.p = [chr, False, False, False, "white"]
       elif chr == "4":
           self.p = [chr, False, False, False, "white"]
       elif chr == "5":
           self.p = [chr, False, False, False, "white"]
       elif chr == WALL_CHAR:
           self.p = [chr, False, False, False, "cyan"]
       elif chr == PLAYER_CHAR:
           self.p = [chr, True, True, True, "orange"]
       elif chr == PLANT:
           self.p = [chr, False, True, False, "green"]
       elif chr == DOOR_CHAR:
           self.p = [chr, True, True, False, "white"]
       elif chr == STAIR_CHAR:
           self.p = [chr, True, True, True, "white"]
       elif chr == "M":
           self.p = [chr, False, False, False, "white"]
       elif chr == "N":
           self.p = [chr, False, False, False, "white"]
       elif chr == SIGHTLINE_CHAR:
           self.p = [chr, False, False, False, "white"]
       elif chr == UNSEEN_CHAR:
           self.p = [chr, False, False, False, "white"]
       elif chr == "I":
           self.p = [chr, True, True, True, "yellow", "item"]
       elif chr == "E":
           self.p = [chr, True, False, True, "white", "entity"]
       elif chr == TEST_CHAR:
           self.p = [chr, True, True, True, "white"]

       self.chr = self.p[0]
       self.clear = self.p[1]
       self.move = self.p[2]
       self.show = self.p[3]
       self.item = "none"
       self.entity = "none"
       self.color = self.p[4]

       if len(self.p) > 5:
           if self.p[5] == "item":
               self.item = Item("none")
               self.chr = self.item.chr

       if len(self.p) > 5:
           if self.p[5] == "entity":
               self.entity = Entity("none")
               self.chr = self.entity.chr
               self.color = self.entity.color

   ##########################################################################################
   def onAction(self, player):
       pOn = ""
       if player[1].chr == STAIR_CHAR: pOn = "nextlevel"
       if player[1].chr == PLANT: player[1] = Tile(AIR_CHAR)
       if player[1].item != "none":
           pOn = "pickup"

       if pOn == "nextlevel":
           printDisplay(newpix, seenpix, player, True)
           print("Will you decend down the stairs?")
           while True:
               print("yes/no")
               decend = input()
               if decend == "yes" or decend == "Yes" or decend == "no" or decend == "No": break
           if decend == "yes" or decend == "Yes":
               return ["s", "done"]

       elif pOn == "pickup":
           message = "You picked up a " + player[1].item.display()
           item = player[1].item
           player[1] = Tile(AIR_CHAR)
           return ["i", message, item]
       return ["none"]


##########################################################################################

class Item():
   def __init__(self, data):
       if data == "none":
           i = randrange(0, 3)
           if i == 0:
               self.type = "weapon"
               self.item = weapons[randrange(0, len(weapons))]
           if i == 1:
               self.type = "potion"
               self.item = potions[randrange(0, len(potions))]
           if i == 2:
               self.type = "armor"
               self.item = armors[randrange(0, len(armors))]

           self.chr = self.item[0]
           self.name = self.item[1]

       else:
           self.item = data[0]
           self.type = data[1]
           self.chr = data[0][0]
           self.name = data[0][1]

   def display(self):
       if self.type == "weapon":
           display = self.item[1] + ", Damage: " + str(self.item[2])
           return display
       elif self.type == "potion":
           if self.item[3] == False:
               display = "Potion of " + self.item[4]
           else:
               display = "Potion of " + self.item[1]
           return display
       elif self.type == "armor":
           display = self.item[1] + ", Defence: " + str(self.item[2])
           return display


def use(self):
   global HP, MAX_HP, STRENGTH
   message = []
   if self.type == "potion":
       if self.item[2] == "heal":
           HP += 4 * STRENGTH
           message += ["You recovered " + str(4 * STRENGTH) + " HP"]
           if HP > MAX_HP: HP = MAX_HP
       elif self.item[2] == "strength":
           STRENGTH += 1
           MAX_HP += 10
           HP += 10
           message += ["Strength +1"]
       elif self.item[2] == "damage":
           HP -= 20
           message += ["You lost 20 HP"]

       if self.item[3] == False:
           self.item[3] = True
           message += ["You discovered " + self.display()]
   return message


class Entity():
   def __init__(self, data):
       if data == "none":
           i = 0
           if i == 0:
               self.type = "enemy"
               self.entity = ["E", "Walking Enemy", 100, 2, 2, 0.5, 0]

           if randrange(0, ENEMY_AWAKE_CHANCE) == 0:
               self.asleep = False
               self.color = "red"
           else:
               self.asleep = True
               self.color = "orange"

           self.chr = self.entity[0]
           self.name = self.entity[1]
           self.path = "none"
           self.see = False

   def display(self):
       display = self.entity[1]
       return display

   def moveEnemy(self, enemy):
       speed = self.entity[5]
       turn = self.entity[6]
       turn += speed
       for m in range(0,int(turn)):
           turn -= 1
           if self.path != "none":
               xy = [enemy[0], enemy[1]]
               txy = [xy[0] + self.path[0][2][0], xy[1] + self.path[0][2][1]]
               if pix[txy[1]][txy[0]].move == True:
                   pix[xy[1]][xy[0]] = enemy[2]
                   enemy[2] = pix[txy[1]][txy[0]]
                   pix[txy[1]][txy[0]] = enemy[3]
                   enemy[0] = enemy[0] + self.path[0][2][0]
                   enemy[1] = enemy[1] + self.path[0][2][1]
                   del self.path[0]
                   if len(self.path) == 0: self.path = "none"
           elif self.asleep == False:
               possibleMoves = [True, True, True, True]
               directions = [[0,-1],[1,0],[0,1],[-1,0]]
               xy = [enemy[0], enemy[1]]
               if pix[xy[1] - 1][xy[0]].move == False: possibleMoves[0] = False
               if pix[xy[1]][xy[0] + 1].move == False: possibleMoves[1] = False
               if pix[xy[1] + 1][xy[0]].move == False: possibleMoves[2] = False
               if pix[xy[1]][xy[0] - 1].move == False: possibleMoves[3] = False

               if possibleMoves.count(True) == 1:
                   for i in range(0,4):
                       if possibleMoves[i] == True: direction = directions[i]
               elif possibleMoves.count(True) >= 2:
                   while True:
                       num = randrange(0,4)
                       if possibleMoves[num] == True:
                           direction = directions[num]
                           break
               else: return enemy

               txy = [xy[0] + direction[0], xy[1] + direction[1]]
               pix[xy[1]][xy[0]] = enemy[2]
               enemy[2] = pix[txy[1]][txy[0]]
               pix[txy[1]][txy[0]] = enemy[3]
               enemy[0] = enemy[0] + direction[0]
               enemy[1] = enemy[1] + direction[1]
       self.entity[6] = turn
       return enemy


##########################################################################################

for i in range(0, 2):
   equiped[i] = Item(equiped[i])
while True:
   pix = mapSize(PIX_LENGTH, PIX_WIDTH, " ")
   pix = prepGen(pix)

   d = errorCheck(startRoom(pix, START_YOFF, START_XOFF))
   pix = d[0]
   rooms = d[1]
   player = d[2]

   d = genRoom(pix, rooms, ROOMS)
   pix = d[0]
   rooms = d[1]
   print("Room gen 100%")

   pix = genTunnelPrep(pix, rooms)
   genTunnels(pix, rooms)
   print("Tunnels 100%")

   genStepActions(pix, rooms)

   pix = replace(pix, "1", "N")
   pix = replace(pix, "4", "N")
   pix = replace(pix, "3", "N")

   if HIDE_ENEMIES == True: hideEnemies()
   seenpix = makeseenpix(pix, player)
   d = rayTrace(pix, player, seenpix)
   newpix = d[0]
   seenpix = d[1]
   seenpix = getSeenPix(newpix, seenpix)

   for i in range(0, 10):
       print()

   done = False
   message = [""]
   while True:
       infoPannel(message)
       message = [""]
       printDisplay(newpix, seenpix, player, True)

       userInput = input()
       if userInput == "r":
           seeMap()
           userInput = ""
       elif userInput == "e":
           message += seeInventory(inventory)
       elif userInput == "q":
           findEnemies()
           userInput = " "

       if DEV:
           if userInput[:2] == "tp":
               userInput = userInput[3:]
               d = devTp(pix, player, userInput.split())
               pix = d[0]
               player = d[1]
               userInput = " "
           elif userInput[:3] == "set":
               userInput = userInput[4:]
               pix = devSet(pix, player[0], userInput.split())
               userInput = " "
           elif userInput[:4] == "fill":
               userInput = userInput[5:]
               pix = devFill(pix, player[0], userInput.split())
               userInput = " "

       for i in range(0, len(userInput)):
           if userInput[i] == "w" or userInput[i] == "a" or userInput[i] == "s" or userInput[i] == "d" or userInput[
               i] == " ":
               direction = userInput[i]

               d = playerMove(pix, player, direction)
               pix = d[0]
               player = d[1]
               message += d[2]

               action = player[1].onAction(player)

               if SIGHT_MEMORY == False:
                   seenpix = makeseenpix(pix, player)

               if HIDE_ENEMIES == True: hideEnemies()
               moveEnemies()
               d = rayTrace(pix, player, seenpix)
               newpix = d[0]
               seenpix = d[1]
               seenpix = getSeenPix(newpix, seenpix)

               if action[0] == "s":
                   floor += 1
                   done = True
               elif action[0] == "i":
                   inventory = addToInventory(action[2], inventory)
                   message += [action[1]]

               if done: break
       if done: break
# CHANGE NEWPIX   ¥




