#include "Judge.h"
#include <string>
#include <iostream>

Judge::Judge(Character* character, Monster* monster, Room* preRoom, Room* nextRoom) {
    this->character = character;
    this->monster = monster;
    this->preRoom = preRoom;
    this->nextRoom = nextRoom;
    if(monster == NULL)
        moveCheck = true;
    else
        moveCheck = 0;
    winOrLost = -1;
    staminaCheck = 0;
}
Judge::Judge(Character* character, Room* preRoom, Room* nextRoom) {
    this->character = character;
    this->preRoom = preRoom;
    this->nextRoom = nextRoom;
    this->monster = NULL;
    moveCheck = 1;
    winOrLost = -1;
    staminaCheck = 0;
}
Judge::~Judge() {
    delete this;
}

void Judge::setMoveCheck(bool moveCheck){
    this->moveCheck = moveCheck;
}
void Judge::setStaminaCheck(int staminaCheck){
    if(staminaCheck > -1 && staminaCheck < 3)
        this->staminaCheck = staminaCheck;
}
void Judge::setWinOrLost(int winOrLost){
    if(winOrLost > -1 && winOrLost < 3)
        this->winOrLost = winOrLost;
}
bool Judge::getMoveCheck(){
    return moveCheck;
}
int Judge::getStaminaCheck(){
    return staminaCheck;
}
int Judge::getWinOrLost(){
    return winOrLost;
}
int Judge::getScore(){
    return character->getScore();
}

string Judge::getMonsterDescription(){
    return monster->longDescription();
}
string Judge::getCharacterDescription(){
    return character->longDescription();
}
string Judge::getNextRoomDescription() {
    return nextRoom->longDescriptionTypically();
}
string Judge::getPreRoomDescription() {
    return preRoom->longDescriptionTypically();
}
Room* Judge::getNextRoom(){
    return nextRoom;
}
Room* Judge::getPreRoom(){
    return preRoom;
}

bool Judge::securityCheck(){
    bool check = false;
    int h1 = character->getHealth();
    int h2 = monster->getHealth();
    int s = character->getStamina();
    if(h1 >= 0 && h1 <= 100)
        if(h2 >= 0 && h2 <= 100)    
            if(s >= 0 && s <= 100)
                check = true;
    if(check == false)
        cout << "There's any parameter in judge is wrong!" << endl;
    return check;
}

// void Judge::fight(Monster* monster, Character* character){
//     int weapon = monster->getWeapon();
//     float score = monster->getScore();
//     if(character->getWeapon() == monster->getWeapon()){
//         monster->setHealth(0);
//         character->decreaseHealth((int)(weapon * 0.1));
//         character->increaseScore((int)(score * 1.5));
//         setMoveCheck(true);
//         setStaminaCheck(0);
//     }
//     else if(character->getWeapon() > weapon){
//         monster->setHealth(0);
//         character->increaseScore((int)score);
//         setMoveCheck(true);
//         setStaminaCheck(0);
//         cout << "[BEHEADED!!!] You triggered a perfect kill! The addition of score multiply 1.5!" << endl;
//     }
//     else{
//         monster->decreaseHealth((int)(character->getWeapon() * 0.6 + 0.5));
//         character->decreaseHealth((int)(weapon * 0.4));
//         setMoveCheck(false);
//         setStaminaCheck(1);
//         cout << "[Info] now Monster HP: " << monster->getHealth() << endl;
//     }
// }
void Judge::fight(){
    int weapon = monster->getWeapon();
    // float score = monster->getScore();
    if(character->getWeapon() == monster->getWeapon()){
        monster->setHealth(0);
        character->decreaseHealth((int)(weapon * 0.1));
        // character->increaseScore((int)(score * 1.5));
        setMoveCheck(1);
        setStaminaCheck(0);
    }
    else if(character->getWeapon() > weapon){
        monster->setHealth(0);
        // character->increaseScore((int)score);
        setMoveCheck(1);
        setStaminaCheck(0);
        cout << "[BEHEADED!!!] You triggered a perfect kill! The addition of score multiply 1.5!" << endl;
    }
    else{
        monster->decreaseHealth((int)(character->getWeapon() * 0.6 + 0.5));
        character->decreaseHealth((int)(weapon * 0.4));
        setMoveCheck(0);
        setStaminaCheck(1);
        cout << "[Info] now Monster HP: " << monster->getHealth() << endl;
    }
    referee();
    staminaCost();
}

// void Judge::run(Monster* monster, Character* character){
//     character->decreaseHealth((int)(monster->getWeapon() * 0.4 + monster->getHealth() * 0.1));
//     setMoveCheck(0);
//     setStaminaCheck(2);
// }
void Judge::run(){
    character->decreaseHealth((int)(monster->getWeapon() * 0.4 + monster->getHealth() * 0.1));
    setMoveCheck(0);
    setStaminaCheck(2);
    referee();
    staminaCost();
}

int Judge::referee(){
    // staminaCost();

    //玩家状态判断
    if(character->getHealth() <= 0)
        setWinOrLost(0);
    else if(character->getStamina() <= 0)
        setWinOrLost(1);
    else if(character->getScore() >= 80)
        setWinOrLost(2);
    else 
        cout << "Special attitude. " << endl;

    //怪物状态判断
    if(nextRoom->getIsMonsterRoom() == false && monster->getHealth() <= 0){
        setMoveCheck(1);
        character->increaseScore((int)(monster->getScore() + 0.5));
        nextRoom->removeMonster();
    }

    return getWinOrLost();
}

void Judge::staminaCost(){
    int baseCost = (int)(10 + 2.0 * character->getWeight());
    if(staminaCheck == 0){
    }
    else if(staminaCheck == 1){
        baseCost = (int)(0.6 * baseCost + 0.5);
    }
    else if(staminaCheck == 2){
        baseCost = (int)(0.4 * baseCost + 0.5);
    }
    else {
        qDebug() << "staminaCheck in Judge is Wrong";
    }

    if(monster != NULL && monster->tirednessCheck() == true)
        baseCost = (int)(0.8 * baseCost + 0.5);
    character->decreaseStamina(baseCost);
}

Judge operator--(Judge& judge, int num){    //后缀形式
    Judge box = judge;
    judge.staminaCost();
    return box;
}

Judge& operator--(Judge& judge){    //前缀形式
    judge.staminaCost();
    return judge;
}
