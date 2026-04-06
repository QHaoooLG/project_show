#include "item.h" // Include the Item class definition
#include <vector>

class Weapon : public Item {
private:
    int health;
    int stamina;
    int score;
    int weaponValue;

public:
    Weapon(string description, int value, int weightGrams, int health, int stamina, int score, int weaponValue);

    int getHealth();
    void setHealth(int health);
    int getStamina();
    void setStamina(int stamina);
    int getScore();
    void setScore(int score);
    int getWeaponValue();
    void setWeaponValue(int weaponValue);
    string getDescription(string description);
    void createWeapon();
};
