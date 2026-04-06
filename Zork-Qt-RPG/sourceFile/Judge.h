#ifndef JUDGE_H_
#define JUDGE_H_

#include <iostream>
#include "Character.h"
#include "Monster.h"
#include "Room.h"
// #include "ZorkUL.h"
#include <vector>
#include <string>
#include <QDebug>
#include <QString>
using namespace std;

class Judge{
    friend Judge operator--(Judge&, int);   //后缀形式  关于耐力值消耗进行重载
    friend Judge& operator--(Judge&);   //前缀形式

private:
    Character* character;
    Monster* monster;
    Room* preRoom;
    Room* nextRoom;

    //判定状态位
    bool moveCheck; //角色移动标志位 1->可移动 0->不移动
    int staminaCheck;   //耐力值消耗模式
    int winOrLost;  //胜负条件判定

public:
    Judge(Character* character, Monster* monster, Room* preRoom, Room* nextRoom);
    Judge(Character* character, Room* preRoom, Room* nextRoom);
    ~Judge();

    void setMoveCheck(bool moveCheck);
    void setStaminaCheck(int staminaCheck);
    void setWinOrLost(int winOrLost);
    bool getMoveCheck();
    int getStaminaCheck();
    int getWinOrLost();
    int getScore();
    string getMonsterDescription();
    string getCharacterDescription();
    string getNextRoomDescription();
    string getPreRoomDescription();
    Room* getNextRoom();
    Room* getPreRoom();
    
    bool securityCheck();   //检查用于判定的几项参数是否正常，有无超出范围的风险
    void fight(Monster* monster, Character* character); //怪物与玩家交互环节
    void fight();
    void run(Monster* monster, Character* character);
    void run();
    int referee();
    void staminaCost();

};

#endif
