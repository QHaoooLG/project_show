#ifndef ROOM_H_
#define ROOM_H_

#include "item.h"
#include "Monster.h"
#include <map>
#include <string>
#include <vector>
using namespace std;
using std::vector;

class Room
{

private:
	string description;
    map<string, Room *> exits;

    //房间附加类
    Monster* monster;
    vector<Item> itemsInRoom;

    //判定状态位
	bool isPassed;
	bool isMonsterRoom;

	string exitString();	//返回当前房间四个方向分别指向的房间信息

public:
	Room(string description);

	void setExits(Room *north, Room *east, Room *south, Room *west);

	string shortDescription();	//仅返回房间名
	string longDescription();	//打印房间名，房间内所有物品，该房间的出口
	string longDescriptionTypically();	//交互时在弹窗内打印房间信息
	string displayItem();	//打印出房间内所有物品的简短描述
    string getMonsterString();
    int numberOfItems();	//返回房间内物品的数量
    void setIsPassed(bool isPassed);
    bool getIsPassed();
    bool getIsMonsterRoom();    //判断房间是否为怪物房间并返回布尔值

    Monster* getMonster();
    vector<Item>& getRoomItems();

	Room *nextRoom(string direction);	//传入一个方向，返回当前房间在传入方向上的下一房间指针
	void addItem(Item *inItem);	//向房间中添加道具
	int isItemInRoom(string inString);	//从房间道具列表中删除传入道具描述对应的道具: 若房间内道具数量为0则返回false，否则删除指定道具后并返回其在房间道具列表中的下标
    void clearRoomItems();	//清空房间内所有道具
	void addMonster(Monster* monster);	//向房间中添加怪物
    void removeMonster();   //怪物被消灭时调用

};

#endif
