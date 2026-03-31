#include "monsterRoomDialog.h"

monsterRoomDialog::monsterRoomDialog(QWidget *parent):
    QDialog(parent){
        resize(500, 600);
        fightButton = new QPushButton("fight", this);
        runButton = new QPushButton("run", this);
        fightButton->show();
        runButton->show();

        //move(left_distance, top_distance);
        fightButton->move(80, 450);
        runButton->move(280, 450);

        //resize(width, height)
        fightButton->resize(150, 50);
        runButton->resize(150, 50);

        fightButton->setText("Fight");
        runButton->setText("Run");

        connect(fightButton, SIGNAL(clicked()), this, SLOT(on_buttonBox_fight()) );
        connect(runButton, SIGNAL(clicked()), this, SLOT(on_buttonBox_run()) );
}   

monsterRoomDialog::~monsterRoomDialog(){
    delete this;
}   

void monsterRoomDialog::on_buttonBox_fight(){
    // if(judge->getNextRoom()->getMonster() == NULL)
    judge->fight();
    done(judge->getMoveCheck());
}

void monsterRoomDialog::on_buttonBox_run(){
    judge->run();
    done(judge->getMoveCheck());
}

void monsterRoomDialog::setJudge(Judge* judge){
    this->judge = judge;
    label = new QLabel("label", this);
    label->resize(350, 350);
    label->move(80, 20);
    string str = "---------- [MonsterRoom] ----------\n";
    string roomStr = judge->getNextRoomDescription();
    string monsterStr = judge->getMonsterDescription();
    string characterStr = judge->getCharacterDescription();
    str += roomStr + monsterStr + characterStr;
    QString qstr = QString::fromStdString(str);
    label->setText(qstr);
}

void QDialog::closeEvent(QCloseEvent *e){
    done(-1);
}
