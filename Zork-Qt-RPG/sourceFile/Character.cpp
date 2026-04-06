#include "Character.h"
#include "item.h"
#include <string>

Character::Character(string name, int health, int stamina) {
    this->name = name;
    this->health = health;
    this->stamina = stamina;
    score = 0;
    weaponSum = 10;
    this->weight = 1;
}

string Character::getName() {
    return name;
}
void Character::setName(string name) {
    this->name = name;
}

int Character::getHealth() {
    return health;
}
int Character::getStamina() {
    return stamina;
}
int Character::getScore(){
    return score;
}
int Character::getWeapon(){
    return weaponSum;
}
int Character::getWeight(){
    return weight;
}

void Character::increaseStamina(int amount) {
    stamina += amount;
}
void Character::decreaseStamina(int amount) {
    stamina -= amount;
}
void Character::increaseHealth(int amount) {
    health += amount;
}
void Character::decreaseHealth(int amount) {
    health -= amount;
}
void Character::increaseScore(int amount) {
    score += amount;
}
void Character::decreaseScore(int amount) {
    score -= amount;
}
string Character::getPlayerStatus()
{
    return "--- [Player Status] ---\n" + longDescription();
}

string Character::longDescription(){
    string description = "\n----- [Character Status] -----";
    description += "\n| [Character Name] " + this->name;
    description += "\n| [Health] " + to_string(this->getHealth());
    description += "\n| [Stamina] " + to_string(this->stamina);
    description += "\n| [Weapon] " + to_string(this->weaponSum);
    description += "\n| [Score] " + to_string(this->score);
    description += "\n| [Weight] " + to_string(this->weight);
    description += "\n| [Item List]\n";
    int cnt = 1;
    for (vector<Item>::iterator i = package.begin(); i != package.end(); i++){
        description += "| [Item # " + to_string(cnt++) + "] " + (*i).getLongDescription() + "\n";
    }
    return description;
}

void Character::addItems(Item &item) {
    package.push_back(item);
    health+=item.getHealth();
    stamina+=item.getStamina();
    weaponSum+=item.getWeaponValue();
    weight+=item.getWeight();
    score+=item.getScore();
    if(item.getWeaponCheck() == 1)
      this->weaponSum += (int)item.getWeaponValue()+0.5;
}

void Character::getItems(Room& room)
{
    vector<Item>& items=room.getRoomItems();
    if(items.size() > 1)
        items.pop_back();
    if(items.size() != 0){
        for (Item& item : items) {
            this->addItems(item);
            room.isItemInRoom(item.getShortDescription()); 
        }
    }
    room.clearRoomItems();
}
