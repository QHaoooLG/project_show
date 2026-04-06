#include "gameoverDialog.h".h"

gameoverDialog::gameoverDialog(QWidget *parent):
    QDialog(parent){
    resize(500, 600);
    okButton = new QPushButton("ok", this);
    okButton->show();

    //move(left_distance, top_distance);
    okButton->move(80, 450);

    //resize(width, height)
    okButton->resize(150, 50);

    okButton->setText("OK");

    connect(okButton, SIGNAL(clicked()), this, SLOT(on_buttonBox_ok()) );
}

gameoverDialog::~gameoverDialog(){
    delete this;
}

void gameoverDialog::on_buttonBox_ok(){
    done(0);
}

void gameoverDialog::setJudge(Judge* judge){
    this->judge = judge;
    label = new QLabel("label", this);
    label->resize(350, 350);
    label->move(80, 20);
    string str = "";
    str += "---------- [GAMEOVER] ----------\n";
    if(judge->getWinOrLost() == 0){
        // str += zork->player->getPlayerStatus();
        str += "\nYou are died!";
        str += "\nYour score : " + to_string(judge->getScore());
    }
    else if(judge->getWinOrLost() == 1){
        str += "\nYou are still alive without any stamina to move";
        str += "\nYour score : " + to_string(judge->getScore());
    }
    else if(judge->getWinOrLost() == 2){
        str += "\n[Hidden Ending] You reached the perfect success!";
        str += "\nYour score : " + to_string(judge->getScore());
    }
    else{
        str += "@@@ ERROR @@@\n";
        str += "Wrong in variable of winOrLost";
        qDebug() << tr("error");
    }
    QString qstr = QString::fromStdString(str);
    label->setText(qstr);
}
