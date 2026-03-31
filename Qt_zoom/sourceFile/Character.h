#ifndef CHARACTER_H_
#define CHARACTER_H_

#include <string>
#include "Room.h"
#include "item.h"
using namespace std;
#include <vector>
using std::vector;


class Character {
private:
    string name;    //玩家名
    int health; //健康度
    int stamina;    //耐力值
    int score;  //得分
    vector<Item> package;   //背包
    int weaponSum;  //玩家武力值
    int weight; //玩家背包中物品总重量

public:
    Character(string name, int health, int stamina);

    string longDescription();
    void setName(string name);
    string getName();
    int getHealth();
    int getStamina();
    int getScore();
    int getWeapon();
    void getItems(Room& room);
    int getWeight();

    void increaseHealth(int amount);
    void decreaseHealth(int amount);
    void increaseStamina(int amount);
    void decreaseStamina(int amount);
    void increaseScore(int amount);
    void decreaseScore(int amount);

    void addItems(Item &item);
    int addHealth(Item &item);
    int addStamina(Item &item);
    int addScore(Item &item);
    int addWeaponSum(Item &item);
    int addValue(Item &item);
    int addWeight(Item &item);

    string getPlayerStatus();

};

#endif /*CHARACTER_H_*/

