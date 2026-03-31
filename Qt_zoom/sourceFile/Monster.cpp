#include "Monster.h"
#include <iostream>
using namespace std;

Monster::Monster(string inDescription, int inHealth, int inWeapon, float inScore){
    health = inHealth;
    description = inDescription;
    weapon = inWeapon;
    score = inScore;
    this->tiredness = 0;
}

string Monster::shortDescription(){
    return description;
}
string Monster::longDescription(){
    string description = "\n----- [Monster Status] -----";
    description += "\n| [Monster Name] " + this->description;
    description += "\n| [Health] " + to_string(this->getHealth());
    description += "\n| [Weapon] " + to_string(this->getWeapon());
    description += "\n| [Score] " + to_string(this->score);
    description += "\n";
    return description;
}

int Monster::getHealth(){
    return health;
}
int Monster::getWeapon(){
    return weapon;
}
float Monster::getScore(){
    return score;
}
void Monster::increaseHealth(int amount) {
    health += amount;
}
void Monster::decreaseHealth(int amount) {
    health -= amount;
}
void Monster::setHealth(int health) {
    this->health = health;
}

bool Monster::tirednessCheck(){
    if(health <= 0)
        cout << "Monster has been killed" << endl;
    else if(health > (int)health*0.75)
        tiredness = false;
    else 
        tiredness = true;
    return tiredness;
}

