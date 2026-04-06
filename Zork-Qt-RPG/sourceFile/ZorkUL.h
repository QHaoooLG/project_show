#ifndef ZORKUL_H_
#define ZORKUL_H_

#include "Command.h"
#include "Parser.h"
#include "Room.h"
#include "item.h"
#include "Character.h"
#include <iostream>
#include <string>
using namespace std;

class ZorkUL
{
private:
	Parser parser;

	void randomInit();
    void roguelike();

	void createRooms();
	void createItems();
	void createCharacter();
	void createItem();

	bool processCommand(Command command);
	void goRoom(Command command);
	void goName(string result);

	void printWelcome();
	void printHelp();
	void displayItems();
	
    // vector<Room*> teleRooms;    //存储所有创建的房间，用于随机传送
    // vector<Monster*> teleMonsters;
 //    vector<Item*> teleItems;
	vector<Item*> itemList;	//游戏初始化时存储游戏中定义的所有道具
    vector<Monster*> monsterList;
    vector<Room*> roomList;

public:
	ZorkUL();
	void play();
    void init();    //肉鸽特性初始化

	Room *currentRoom;
	Character *player;

	string go(string direction);
    string goWindowRoom(string direction);  //实现GUI界面的走房间功能
    Room* teleport();  //随机选择房间并返回其详细描述
    string showMap();	//在TextEdit中打印地图

	void teleportMonster(Room *room);
    void teleportItem(Room *room);
    void teleportSum(Room *room);
    
};

#endif /*ZORKUL_H_*/
