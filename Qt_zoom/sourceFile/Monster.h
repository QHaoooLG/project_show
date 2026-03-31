#ifndef MONSTER_H_
#define MONSTER_H_

// #include "Character.h"
// #include "Judge.h"
#include <map>
#include <string>
#include <vector>
using namespace std;

class Monster{

private:
	string description;
	int health;
    int weapon;
	float score;
	bool tiredness;

public:
	Monster(string description, int health, int weapon, float score);

	string shortDescription();
	string longDescription();
	int getHealth();
	int getWeapon();
	float getScore();
	void increaseHealth(int amount);
    void decreaseHealth(int amount);
	void setHealth(int amount);

    bool tirednessCheck();

};

#endif
