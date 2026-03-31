#include "Food.h"

Food::Food(string description, int value, int weightGrams, int health, int stamina,int score,int weaponValue)
    : Item(description, value, weightGrams, health, stamina, score, weaponValue) {}

int Food::getHealth() {
    return health;
}

void Food::setHealth(int health) {
    this->health = health;
}

int Food::getStamina() {
    return stamina;
}

void Food::setStamina(int stamina) {
    this->stamina = stamina;
}
string Food::getDescription(string description)
{
    return description;
}
int Food::getScore() {
    return score;
}

void Food::setScore(int score) {
    this->score = score;
}
int Food::getWeaponValue()
{
    return weaponValue;
}
void Food::setWeaponValue(int weaponValue)
{
    this->weaponValue=weaponValue;
}

