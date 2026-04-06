#include "item.h" // Include the Item class definition
#include <vector>

class Scholarism : public Item {
private:
    int health;
    int stamina;
    int score;
    int weaponValue;

public:
    Scholarism(string description, int value, int weightGrams, int health, int stamina, int score, int weaponValue);

    int getHealth();
    void setHealth(int health);
    int getStamina();
    void setStamina(int stamina);
    int getScore();
    void setScore(int score);
    int getWeaponValue();
    void setWeaponValue(int weaponValue);
    string getDescription(string description);
    void createScholarism();
};
