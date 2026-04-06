/*
1.新添加一个房间
在create room中写入
2.加入一条指令使游戏能够随机输出一个房间
使用switch-case输出房间
3.显示出房间的的位置
可以借鉴take中的location给每个房间标号，从而传达出房间的具体路径
*/
#include <iostream>
#include <ctime>
#include <cstdlib>

using namespace std;

#include "Room.h"
#include "ZorkUL.h"
#include "Food.h"
#include "Weapon.h"
#include "Scholarism.h"
#include "item.h"
#include "Monster.h"
#include "Judge.h"
#include "Character.h"

ZorkUL::ZorkUL()
{
    // init();
    // randomInit();
    createRooms();
    createCharacter();
}

void ZorkUL::init(){
    Room *a, *b, *c, *d, *e, *f, *g, *h, *i, *j;
    a = new Room("a");
    b = new Room("b");
    c = new Room("c");
    d = new Room("d");
    e = new Room("e");
    f = new Room("f");
    g = new Room("g");
    h = new Room("h");
    i = new Room("i");
    j = new Room("j");

    Item* duckNeck_actedByMouse=new Food("duckNeck_actedByMouse",0,0,-20, -20, -20, 0);
    Item* fryPancake=new Food("fryPancake",0,0, 10, 10, 10, 0.0);
    Item* Barbecue=new Food("Barbecue",0,0, 20, 20, 20, 0.0);
    Item* like_fromOppositeSex=new Food("like_fromOppositeSex",0,0, 30, 30, 10, 10.0);
    Item* bigIceCream=new Food("bigIceCream",0,0, -10, 30, 0, -5.0);

    Item* sci_firstRegion=new Scholarism("sci_firstRegion",0,1,0,-10,50,10);
    Item* academicGarbage=new Scholarism("academicGarbage",0,0,10,10,-10,0);
    Item* approve_fromTutor=new Scholarism("approve_fromTutor",0,0,0,20,10,5);
    Item* pressure_fromTutor=new Scholarism("pressure_fromTutor",0,2,-10,-20,10,0);

    Item* logitechMouse=new Weapon("logitechMouse",0,1,0,10,10,20);
    Item* pillow_CSstudent=new Weapon("pillow_CSstudent",0,1,0,20,10,10);
    Item* flamingSinglechip=new Weapon("flamingSinglechip",0,1,0,-10,20,30);
    Item* trackingCarDashing=new Weapon("trackingCarDashing",0,2,0,-20,30,30);
    Item* excellentKeyboard=new Weapon("excellentKeyboard",0,2,0,20,20,40);

    Monster* lovelorn_collegeBoy = new Monster("lovelorn_college", 20, 30, 30.0);
    Monster* bugWarningCrash = new Monster("bugWarningCrash", 40, 40, 50.0);
    Monster* cockroachInDormitory = new Monster("cockroachInDormitory", 50, 20, 10.0);

    itemList.push_back(duckNeck_actedByMouse);
    itemList.push_back(fryPancake);
    itemList.push_back(Barbecue);
    itemList.push_back(like_fromOppositeSex);
    itemList.push_back(bigIceCream);
    itemList.push_back(sci_firstRegion);
    itemList.push_back(academicGarbage);
    itemList.push_back(approve_fromTutor);
    itemList.push_back(pressure_fromTutor);
    itemList.push_back(logitechMouse);
    itemList.push_back(pillow_CSstudent);
    itemList.push_back(flamingSinglechip);
    itemList.push_back(trackingCarDashing);
    itemList.push_back(excellentKeyboard);

    monsterList.push_back(lovelorn_collegeBoy);
    monsterList.push_back(bugWarningCrash);
    monsterList.push_back(cockroachInDormitory);

    a->setExits(f, b, d, c);
    b->setExits(NULL, j, NULL, a);
    c->setExits(NULL, a, NULL, NULL);
    d->setExits(a, e, NULL, i);
    e->setExits(NULL, NULL, NULL, d);
    f->setExits(NULL, g, a, h);
    g->setExits(NULL, NULL, NULL, f);
    h->setExits(NULL, f, NULL, NULL);
    i->setExits(NULL, d, NULL, NULL);
    j->setExits(NULL, NULL, NULL, b);

    roomList.push_back(a);
    roomList.push_back(b);
    roomList.push_back(c);
    roomList.push_back(d);
    roomList.push_back(e);
    roomList.push_back(f);
    roomList.push_back(g);
    roomList.push_back(h);
    roomList.push_back(i);
    roomList.push_back(j);

    roguelike();

    // currentRoom = a;
}

// void ZorkUL::randomInit(){
//     Room *a, *b, *c, *d, *e, *f, *g, *h, *i, *j;
//     Item* duckNeck_actedByMouse=new Food("duckNeck_actedByMouse",0,0,-20, -20, -20, 0);
//     Item* fryPancake=new Food("fryPancake",0,0, 10, 10, 10, 0.0);
//     Item* Barbecue=new Food("Barbecue",0,0, 20, 20, 20, 0.0);
//     Item* like_fromOppositeSex=new Food("like_fromOppositeSex",0,0, 30, 30, 10, 10.0);
//     Item* bigIceCream=new Food("bigIceCream", 0, 0, -10, 30, 0, -5.0);

//     Item* sci_firstRegion=new Scholarism("sci_firstRegion",0,1,0,-10,50,10);
//     Item* academicGarbage=new Scholarism("academicGarbage",0,0,10,10,-10,0);
//     Item* approve_fromTutor=new Scholarism("approve_fromTutor",0,0,0,20,10,5);
//     Item* pressure_fromTutor=new Scholarism("pressure_fromTutor",0,2,-10,-20,10,0);

//     Item* logitechMouse=new Weapon("logitechMouse",0,1,0,10,10,20);
//     Item* pillow_CSstudent=new Weapon("pillow_CSstudent",0,1,0,20,10,10);
//     Item* flamingSinglechip=new Weapon("flamingSinglechip",0,1,0,-10,20,30);
//     Item* trackingCarDashing=new Weapon("trackingCarDashing",0,2,0,-20,30,30);
//     Item* excellentKeyboard=new Weapon("excellentKeyboard",0,2,0,20,20,40);

//     Monster* lovelorn_collegeBoy = new Monster("lovelorn_college", 20, 30, 30.0);
//     Monster* bugWarningCrash = new Monster("bugWarningCrash", 40, 40, 50.0);
//     Monster* cockroachInDormitory = new Monster("cockroachInDormitory", 50, 20, 10.0);

//     teleItems.push_back(duckNeck_actedByMouse);
//     teleItems.push_back(fryPancake);
//     teleItems.push_back(Barbecue);
//     teleItems.push_back(like_fromOppositeSex);
//     teleItems.push_back(bigIceCream);
//     teleItems.push_back(sci_firstRegion);
//     teleItems.push_back(academicGarbage);
//     teleItems.push_back(approve_fromTutor);
//     teleItems.push_back(pressure_fromTutor);
//     teleItems.push_back(logitechMouse);
//     teleItems.push_back(pillow_CSstudent);
//     teleItems.push_back(flamingSinglechip);
//     teleItems.push_back(trackingCarDashing);
//     teleItems.push_back(excellentKeyboard);

//     teleMonsters.push_back(lovelorn_collegeBoy);
//     teleMonsters.push_back(bugWarningCrash);
//     teleMonsters.push_back(cockroachInDormitory);

//     itemList.push_back(duckNeck_actedByMouse);
//     itemList.push_back(fryPancake);
//     itemList.push_back(Barbecue);
//     itemList.push_back(like_fromOppositeSex);
//     itemList.push_back(bigIceCream);
//     itemList.push_back(sci_firstRegion);
//     itemList.push_back(academicGarbage);
//     itemList.push_back(approve_fromTutor);
//     itemList.push_back(pressure_fromTutor);
//     itemList.push_back(logitechMouse);
//     itemList.push_back(pillow_CSstudent);
//     itemList.push_back(flamingSinglechip);
//     itemList.push_back(trackingCarDashing);
//     itemList.push_back(excellentKeyboard);

//     a = new Room("a");
//     teleportSum(a);

//     b = new Room("b");
//     teleportSum(b);

//     c = new Room("c");
//     teleportSum(c);

//     d = new Room("d");
//     teleportSum(d);

//     e = new Room("e");
//     teleportSum(e);

//     f = new Room("f");
//     teleportSum(f);

//     g = new Room("g");
//     teleportSum(g);

//     h=new Room("h");
//     teleportSum(h);

//     i = new Room("i");
//     teleportSum(i);

//     j = new Room("j");
//     teleportSum(j);

//     a->setExits(f, b, d, c);
//     b->setExits(NULL, j, NULL, a);
//     c->setExits(NULL, a, NULL, NULL);
//     d->setExits(a, e, NULL, i);
//     e->setExits(NULL, NULL, NULL, d);
//     f->setExits(NULL, g, a, h);
//     g->setExits(NULL, NULL, NULL, f);
//     h->setExits(NULL, f, NULL, NULL);
//     i->setExits(NULL, d, NULL, NULL);
//     j->setExits(NULL, NULL, NULL, b);

//     teleRooms.push_back(a);
//     teleRooms.push_back(b);
//     teleRooms.push_back(c);
//     teleRooms.push_back(d);
//     teleRooms.push_back(e);
//     teleRooms.push_back(f);
//     teleRooms.push_back(g);
//     teleRooms.push_back(h);
//     teleRooms.push_back(i);
//     teleRooms.push_back(j);

//     currentRoom = a;
// }
// 创建房间，输入房间里的东西，告知各个房间怎么走
void ZorkUL::createRooms()
{
	Room *a, *b, *c, *d, *e, *f, *g, *h, *i, *j;

    Item* duckNeck_actedByMouse=new Food("duckNeck_actedByMouse",0,0,-20, -20, -20, 0);
    Item* fryPancake=new Food("fryPancake",0,0, 10, 10, 10, 0.0);
    Item* Barbecue=new Food("Barbecue",0,0, 20, 20, 20, 0.0);
    Item* like_fromOppositeSex=new Food("like_fromOppositeSex",0,0, 30, 30, 10, 10.0);
    Item* bigIceCream=new Food("bigIceCream",0,0, -10, 30, 0, -5.0);

    Item* sci_firstRegion=new Scholarism("sci_firstRegion",0,1,0,-10,50,10);
    Item* academicGarbage=new Scholarism("academicGarbage",0,0,10,10,-10,0);
    Item* approve_fromTutor=new Scholarism("approve_fromTutor",0,0,0,20,10,5);
    Item* pressure_fromTutor=new Scholarism("pressure_fromTutor",0,2,-10,-20,10,0);

    Item* logitechMouse=new Weapon("logitechMouse",0,1,0,10,10,20);
    Item* pillow_CSstudent=new Weapon("pillow_CSstudent",0,1,0,20,10,10);
    Item* flamingSinglechip=new Weapon("flamingSinglechip",0,1,0,-10,20,30);
    Item* trackingCarDashing=new Weapon("trackingCarDashing",0,2,0,-20,30,30);
    Item* excellentKeyboard=new Weapon("excellentKeyboard",0,2,0,20,20,40);

	Monster* lovelorn_collegeBoy = new Monster("lovelorn_college", 20, 30, 30.0);
	Monster* bugWarningCrash = new Monster("bugWarningCrash", 40, 40, 50.0);
	Monster* cockroachInDormitory = new Monster("cockroachInDormitory", 50, 20, 10.0);

    a = new Room("a");
    a->addItem(duckNeck_actedByMouse);
    a->addItem(trackingCarDashing);

	b = new Room("b");
    b->addItem(fryPancake);
    b->addItem(pillow_CSstudent);
	b->addMonster(cockroachInDormitory);

	c = new Room("c");
    c->addItem(Barbecue);
    c->addItem(flamingSinglechip);

	d = new Room("d");
    d->addItem(bigIceCream);

	e = new Room("e");
    e->addItem(sci_firstRegion);

	f = new Room("f");
    f->addItem(like_fromOppositeSex);
	f->addMonster(lovelorn_collegeBoy);

	g = new Room("g");
    g->addItem(approve_fromTutor);

	h = new Room("h");
    h->addItem(logitechMouse);
    h->addItem(excellentKeyboard);
	h->addMonster(bugWarningCrash);

	i = new Room("i");
    i->addItem(pressure_fromTutor);

	j = new Room("j");
    j->addItem(academicGarbage);

    //  告知房间位置           (North, East, South, West)
	a->setExits(f, b, d, c);
    b->setExits(NULL, j, NULL, a);
	c->setExits(NULL, a, NULL, NULL);
	d->setExits(a, e, NULL, i);
	e->setExits(NULL, NULL, NULL, d);
	f->setExits(NULL, g, a, h);
	g->setExits(NULL, NULL, NULL, f);
	h->setExits(NULL, f, NULL, NULL);
	i->setExits(NULL, d, NULL, NULL);
	j->setExits(NULL, NULL, NULL, b);

    //在ZorkUL.h中定义vector<Room*> roomList;
    //当所有房间被创建时，同时也将这些房间添加到roomList这个vector数组中以便后续进行随机选取
    roomList.push_back(a);
    roomList.push_back(b);
    roomList.push_back(c);
    roomList.push_back(d);
    roomList.push_back(e);
    roomList.push_back(f);
    roomList.push_back(g);
    roomList.push_back(h);
    roomList.push_back(i);
    roomList.push_back(j);

    itemList.push_back(duckNeck_actedByMouse);
    itemList.push_back(fryPancake);
    itemList.push_back(Barbecue);
    itemList.push_back(like_fromOppositeSex);
    itemList.push_back(bigIceCream);
    itemList.push_back(sci_firstRegion);
    itemList.push_back(academicGarbage);
    itemList.push_back(approve_fromTutor);
    itemList.push_back(pressure_fromTutor);
    itemList.push_back(logitechMouse);
    itemList.push_back(pillow_CSstudent);
    itemList.push_back(flamingSinglechip);
    itemList.push_back(trackingCarDashing);
    itemList.push_back(excellentKeyboard);

	currentRoom = a;
}

void ZorkUL::createCharacter() {
	player = new Character("Player", 100, 200);
}

/**
 *  Main play routine.  Loops until end of play.
 * 主要游戏程序。循环直到游戏结束
 */
void ZorkUL::play()
{
	printWelcome();

	// Enter the main command loop.  Here we repeatedly read commands and
	// execute them until the ZorkUL game is over.
	// 进入主命令循环。在这里，我们反复阅读命令和执行它们，直到ZorkUL游戏结束。
	bool finished = false;
	while (!finished)
	{
		// Create pointer to command and give it a command.
		// 创建指向命令的指针并给它一个命令
		Command *command = parser.getCommand();
		// Pass dereferenced command and check for end of game.
		// 传递取消引用的命令并检查游戏是否结束。
		finished = processCommand(*command);
		// Free the memory allocated by "parser.getCommand()"
		// 释放“parser.getCommand（）”分配的内存
		//   with ("return new Command(...)")
		delete command;
	}
	cout << endl;
	cout << "end" << endl;
}

void ZorkUL::printWelcome()
{
	cout << "start" << endl;
	cout << "info for help" << endl;
	cout << endl;
	cout << currentRoom->longDescription() << endl;
}

/**
 * Given a command, process (that is: execute) the command.
 * If this command ends the ZorkUL game, true is returned, otherwise false is
 * returned.
 * 给定一个命令，处理（即：执行）该命令，如果此命令结束ZorkUL游戏，则返回true，否则返回false。
 */
bool ZorkUL::processCommand(Command command)
{
	if (command.isUnknown())
	{
		cout << "invalid input" << endl;
		return false;
	}

	string commandWord = command.getCommandWord();
	// 用得到的word与info做比较
	// compare()函数，compare函数是逐个字符比较（比较的是ASCII码），一旦不相同就会输出结果;一旦如果字符串相等就输出0;1则是前者大于后者;-1与之相反
	if (commandWord.compare("info") == 0)
		printHelp();

	else if (commandWord.compare("map") == 0)
	{
		cout << "[h] --- [f] --- [g]" << endl;
        cout << "         |         " << endl;
        cout << "         |         " << endl;
		cout << "[c] --- [a] --- [b] --- [j]" << endl;
        cout << "         |         " << endl;
        cout << "         |         " << endl;
        cout << "[i] --- [d] --- [e]" << endl;
	}

	else if (commandWord.compare("go") == 0)
		goRoom(command);

	else if (commandWord.compare("take") == 0)
	{
		if (!command.hasSecondWord())
		{
			cout << "incomplete input" << endl;
		}
		else if (command.hasSecondWord())
		{
			cout << "you're trying to take " + command.getSecondWord() << endl;
			int location = currentRoom->isItemInRoom(command.getSecondWord());
			if (location < 0)
				cout << "item is not in room" << endl;
			else
				cout << "item is in room" << endl;
			cout << "index number " << +location << endl;
			cout << endl;
			cout << currentRoom->longDescription() << endl;
		}
	}

	else if (commandWord.compare("put") == 0)
	{
	}
	/*
	{
	if (!command.hasSecondWord()) {
		cout << "incomplete input"<< endl;
		}
		else
			if (command.hasSecondWord()) {
			cout << "you're adding " + command.getSecondWord() << endl;
			itemsInRoom.push_Back;
		}
	}
*/
	else if (commandWord.compare("quit") == 0)
	{
		if (command.hasSecondWord())
			cout << "overdefined input" << endl;
		else
			return true; /**signal to quit*/
	}
	return false;
}
/** COMMANDS **/
void ZorkUL::printHelp()
{
	cout << "valid inputs are; " << endl;
	parser.showCommands();
}

void ZorkUL::goRoom(Command command)
{
	if (!command.hasSecondWord())
	{
		cout << "incomplete input" << endl;
		return;
	}

	string direction = command.getSecondWord();

	// Try to leave current room.
	// 尝试离开当前的房间，创建一个指针来到达下一个房间
	Room *nextRoom = currentRoom->nextRoom(direction);

	if (nextRoom == NULL)
		cout << "underdefined input" << endl;
	else
	{
		// 将下一个房间的地址赋给当前房间来到达下一个房间
		currentRoom = nextRoom;
		cout << currentRoom->longDescription() << endl;
	}
}

string ZorkUL::go(string direction)
{
	// Make the direction lowercase
	// transform(direction.begin(), direction.end(), direction.begin(),:: tolower);
	// Move to the next room
	Room *nextRoom = currentRoom->nextRoom(direction);
	if (nextRoom == NULL)
		return ("direction null");
	else
	{
		currentRoom = nextRoom;
		return currentRoom->longDescription();
	}
}

string ZorkUL::showMap(){
    string map0 = "\n---------------------------\n";
    string map1 = "[h] --- [f] --- [g]\n";
    string map2 = "         |         \n";
    string map3 = "         |         \n";
    string map4 = "[c] --- [a] --- [b] --- [j]\n";
    string map5 = "         |         \n";
    string map6 = "         |         \n";
    string map7 = "[i] --- [d] --- [e]\n";
    string map8 = "----------------------------\n";
    string currentLocation = "";
    currentLocation += "[Your Location] Room [" + currentRoom->shortDescription() + "]\n";
    currentLocation += "----------------------------\n";
    string str = map0 + map1 + map2 + map3 + map4 + map5 + map6 + map7 + map8 + currentLocation;
    return str;
}

string ZorkUL::goWindowRoom(string direction)
{
    Room* nextRoom=currentRoom->nextRoom(direction);
    if(nextRoom==NULL)
    {
        return "[Warning] Hit the wall!";
    }
    else
    {
        Judge* judge = new Judge(player, nextRoom->getMonster(), currentRoom, nextRoom);

        // if(judge->getMoveCheck() == false)
        //     return ;
        
        currentRoom=nextRoom;
        player->getItems(*currentRoom);
        string s=player->longDescription()+currentRoom->longDescription();
        return s;
    }                                                                    
}

Room* ZorkUL::teleport()
{
    srand(time(NULL));
    int random = rand() % roomList.size();
    currentRoom = roomList[random];
    return currentRoom;
}

void ZorkUL::roguelike(){
    srand(time(0));

    //物品随机初始化
    for(int i=0; i<itemList.size(); i++){
        bool assign = false;
        while(assign == false){
            srand(time(NULL));
            int random = rand() % roomList.size();
            if(roomList[random]->numberOfItems() < 3){
                roomList[random]->addItem(itemList[i]);
                assign = true;
            }
        }
    }

    //怪物随机初始化
    for(int i=0; i<monsterList.size(); i++){
        bool assign = false;
        while(assign == false){
            srand(time(NULL));
            int random = rand() % monsterList.size();
            if(roomList[random]->getMonster() == NULL && roomList[random]->getIsMonsterRoom() == false){
                roomList[random]->addMonster(monsterList[i]);
                assign = true;
            }
        }
    }

    //人物位置初始化
    int charaterAssign = false;
    while(charaterAssign == false){
        srand(time(NULL));
        int random = rand() % roomList.size();
        if(roomList[random]->getIsMonsterRoom() == false){
            currentRoom = roomList[random];
            charaterAssign = true;
        }
    }
}
