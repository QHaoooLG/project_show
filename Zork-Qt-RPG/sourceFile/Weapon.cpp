#include "Weapon.h"

Weapon::Weapon(string description, int value, int weightGrams, int health, int stamina,int score,int weaponValue)
    : Item(description, value, weightGrams, health, stamina, score, weaponValue) {}

int Weapon::getHealth() {
    return health;
}

void Weapon::setHealth(int health) {
    this->health = health;
}

int Weapon::getStamina() {
    return stamina;
}

void Weapon::setStamina(int stamina) {
    this->stamina = stamina;
}
string Weapon::getDescription(string description)
{
    return description;
}
int Weapon::getScore() {
    return score;
}

void Weapon::setScore(int score) {
    this->score = score;
}
int Weapon::getWeaponValue()
{
    return weaponValue;
}
void Weapon::setWeaponValue(int weaponValue)
{
    this->weaponValue=weaponValue;
}

