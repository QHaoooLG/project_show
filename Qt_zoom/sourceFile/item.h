#ifndef ITEM_H_
#define ITEM_H_

#include <map>
#include <string>
#include <iostream>
using namespace std;

class Item {
private:
    //道具基础属性
    string description; //物品名
    string longDescription; //物品详细描述
    int weightGrams;    //物品重量
    int value;    //物品价值
    bool weaponCheck;   //该物品是否为武器类型 1->武器 0->非武器

    //道具效果值
    int health;
    int stamina;
    int score;
    int weaponValue;    //武器武力值

public:
    Item(string description, int value, int weightGrams, int health, int stamina, int score, int weaponValue);
    Item (string description);

    virtual int getWeaponValue();
	string getShortDescription();
    string getLongDescription();
	int getWeight();
	void setWeight(int weightGrams);
    int getValue();
	void setValue(int value);
	int getWeaponCheck();
    void setWeapon(int weapon);
    int getHealth();
    int getStamina();
    int getScore();
    
};

#endif /*ITEM_H_*/
