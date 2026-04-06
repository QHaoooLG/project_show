#include "item.h"

Item::Item(string description, int value, int weightGrams, int health, int stamina, int score, int weaponValue) {
	this->description = description;
    this->score = score;
	setWeight(weightGrams);
    this->health = health;
    this->stamina = stamina;
    setWeapon(weaponValue);
	setValue(value);
}
Item::Item(string inDescription) {
    description = inDescription;
}

void Item::setWeight(int inWeightGrams)
{
    if (inWeightGrams > 999 || inWeightGrams < 0)
       cout << "weight invalid, must be 0 < weight < 999" ;
    else
	   weightGrams = inWeightGrams;
}
int Item::getWeight(){
    return weightGrams;
}

void Item::setValue(int inValue)
{
    if (inValue > 10 || inValue < 0)
       cout << "value invalid, must be 0 < value < 10" ;
    else
	   value = inValue;
    score = score * (0.1 * inValue + 1.0);
    health = health * (0.1 * inValue + 1.0);
    stamina = stamina * (0.1 * inValue + 1.0);
    weaponValue = weaponValue * (0.1 * inValue + 1.0);
}
int Item::getValue(){
    return value;
}

void Item::setWeapon(int weapon){
    weaponValue = weapon;
    if(weapon > 0)
        weaponCheck = 1;
    else 
        weaponCheck = 0;
}
int Item::getWeaponCheck(){
    if(weaponCheck == 0)
        cout << "Item not a weapon" ;
    else
        cout << "Item is a weapon" ;
    return weaponCheck;
}
int Item::getWeaponValue(){
    return weaponValue;
}
int Item::getHealth()
{
    return health;
}
int Item::getStamina()
{
    return stamina;
}
int Item::getScore()
{
    return score;
}

string Item::getShortDescription()
{
	return description;
}
string Item::getLongDescription()
{
	return " " + description;
}

