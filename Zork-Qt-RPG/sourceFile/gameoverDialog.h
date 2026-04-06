#ifndef GAMEOVERDIALOG_H
#define GAMEOVERDIALOG_H

#include <QDialog>
#include <QMessageBox>
#include <QAbstractButton>
#include <QDebug>
#include <QPushButton>
#include <QLabel>
// #include "ZorkUL.h"
#include "Judge.h"

class gameoverDialog : public QDialog
{
    Q_OBJECT


public:
    explicit gameoverDialog(QWidget *parent = nullptr);
    ~gameoverDialog();

    // void setZork(ZorkUL* zork);
    void setJudge(Judge* judge);

private:
    QPushButton* okButton;
    QLabel* label;

    // ZorkUL* zork;
    Judge* judge;

private slots:
    void on_buttonBox_ok();

};


#endif
