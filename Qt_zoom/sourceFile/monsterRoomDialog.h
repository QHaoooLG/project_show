#ifndef MONSTERROOMDIALOG_H
#define MONSTERROOMDIALOG_H

#include <QDialog>
#include <QMessageBox>
#include <QAbstractButton>
#include <QDebug>
#include <QPushButton>
#include <QLabel>
#include "Judge.h"

class monsterRoomDialog : public QDialog
{
    Q_OBJECT

public:
    explicit monsterRoomDialog(QWidget *parent = nullptr);
    ~monsterRoomDialog();

    void setJudge(Judge* judge);

private:
    QPushButton* fightButton;
    QPushButton* runButton;
    QLabel* label;
    Judge* judge;
 
private slots: 
    void on_buttonBox_fight();
    void on_buttonBox_run();

};


#endif
