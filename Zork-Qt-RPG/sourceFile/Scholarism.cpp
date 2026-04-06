#include "Scholarism.h"

Scholarism::Scholarism(string description, int value, int weightGrams, int health, int stamina,int score,int weaponValue)
    : Item(description, value, weightGrams, health, stamina, score, weaponValue) {}

int Scholarism::getHealth() {
    return health;
}

void Scholarism::setHealth(int health) {
    this->health = health;
}

int Scholarism::getStamina() {
    return stamina;
}

void Scholarism::setStamina(int stamina) {
    this->stamina = stamina;
}
string Scholarism::getDescription(string description)
{
    return description;
}
int Scholarism::getScore() {
    return score;
}

void Scholarism::setScore(int score) {
    this->score = score;
}
int Scholarism::getWeaponValue()
{
    return weaponValue;
}
void Scholarism::setWeaponValue(int weaponValue)
{
    this->weaponValue=weaponValue;
}
