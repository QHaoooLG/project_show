#include "Room.h"
#include "Command.h"

Room::Room(string description)
{
    this->description = description;
    monster = NULL;
    isPassed = false;
    isMonsterRoom = false;
}
// 存储进入房间房间路线方向
void Room::setExits(Room *north, Room *east, Room *south, Room *west)
{
    if (north != NULL)
        exits["north"] = north;
    if (east != NULL)
        exits["east"] = east;
    if (south != NULL)
        exits["south"] = south;
    if (west != NULL)
        exits["west"] = west;
}

string Room::shortDescription()
{
    return description;
}
string Room::longDescription()
{
    return "room = " + description + ".\n" + displayItem() + "\n" + exitString();
}
string Room::longDescriptionTypically(){
    string description = "\n----- [Room Information] -----";
    description += "\n| [Room Description] " + this->description;
    // description += "\n| [Exits] ";
    description += "\n| " + exitString();
    description += "\n| [Items in Room] ";
    description += "\n| " + displayItem();
    description += "\n";
    // description += "-----------------\n";
    return description;
}

string Room::exitString()
{
    string returnString = "[Exits] ";
    for (map<string, Room *>::iterator i = exits.begin(); i != exits.end(); i++)
        // Loop through map循环浏览地图
        returnString += "  " + i->first; // access the "first" element of the pair (direction as a string)访问对中的“第一个”元素（方向为字符串）
    return returnString;
}

Room *Room::nextRoom(string direction)
{
    // find按照所给的方向找到结果赋给next，next与exits.end()作比较，因为end()函数返回的是exits最后一个，如果next等于end所返回的，则地图已到边界
    map<string, Room *>::iterator next = exits.find(direction); // returns an iterator for the "pair"返回“对”的迭代器
    if (next == exits.end())
        return NULL;     // if exits.end() was returned, there's no room in that direction.如果返回了exits.end（），那么这个方向就没有空间了
    return next->second; // If there is a room, remove the "second" (Room*)如果有房间，删除“第二个”（房间*）
                         // part of the "pair" (<string, Room*>) and return it.
}

void Room::addItem(Item *inItem)
{
    // cout <<endl;
    // cout << "Just added" + inItem->getLongDescription();
    // 添加房间中的事物
    itemsInRoom.push_back(*inItem);
}

string Room::displayItem()
{
    string tempString = "items in room = ";
    int sizeItems = (itemsInRoom.size());
    if (itemsInRoom.size() < 1)
    {
        tempString = "no items in room";
    }
    else if (itemsInRoom.size() > 0)
    {
        int x = (0);
        for (int n = sizeItems; n > 0; n--)
        {
            // 说明房间里有什么东西
            tempString = tempString + itemsInRoom[x].getShortDescription() + "  ";
            x++;
        }
    }
    return tempString;
}

int Room::numberOfItems()
{
    return itemsInRoom.size();
}

int Room::isItemInRoom(string inString)
{
    int sizeItems = (itemsInRoom.size());
    if (itemsInRoom.size() < 1)
    {
        return false;
    }
    else if (itemsInRoom.size() > 0)
    {
        int x = (0);
        for (int n = sizeItems; n > 0; n--)
        {
            // compare inString with short description
            // 将inString与简短描述进行比较
            int tempFlag = inString.compare(itemsInRoom[x].getShortDescription());
            if (tempFlag == 0)
            {
                // 删除所选的字符
                itemsInRoom.erase(itemsInRoom.begin() + x);
                return x;
            }
            x++;
        }
    }
    return -1;
}

vector<Item>& Room::getRoomItems()
{
    return itemsInRoom;
}

void Room::clearRoomItems()
{
    itemsInRoom.clear();
}

void Room::addMonster(Monster* monster){
    this->monster = monster;
    isMonsterRoom = true;
}

bool Room::getIsMonsterRoom(){
    if(monster == NULL || monster->getHealth() <= 0)
        isMonsterRoom = false;
    return isMonsterRoom;
}

string Room::getMonsterString(){
    string boxstr = "";
    if(isMonsterRoom == true)
        boxstr += "\n[Info] Please enter next room after beat the monster in it.";
    else 
        boxstr += "\n[Info] Entering next room......";
    return boxstr;
}

bool Room::getIsPassed(){
    return isPassed;
}
void Room::setIsPassed(bool isPassed){
    this->isPassed = isPassed;
}

Monster* Room::getMonster() {
    return monster;
}

void Room::removeMonster(){
    monster = NULL;
    isMonsterRoom = false;
}
