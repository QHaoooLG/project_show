#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "ZorkUL.h"
#include "Judge.h"

#include <QTimer>
#include <QDialog>

/*  Lambda表达式
 *  Lambda表达式是一种在被调用的位置或作为参数传递给函数的位置定义匿名函数对象（闭包）的简便方法
 *  Lambda表达式的基本语法如下：
 *  [capture list] (parameter list) -> return type { function body }
 *
    1. capture list 是捕获列表，用于指定 Lambda表达式可以访问的外部变量，以及是按值还是按引用的方式访问。
 捕获列表可以为空，表示不访问任何外部变量，也可以使用默认捕获模式 & 或 = 来表示按引用或按值捕获所有外部变量，
 还可以混合使用具体的变量名和默认捕获模式来指定不同的捕获方式。
    2. parameter list 是参数列表，用于表示 Lambda表达式的参数，可以为空，表示没有参数，也可以和普通函数一样指定参数的类型和名称，
还可以在 c++14 中使用 auto 关键字来实现泛型参数。
    3. return type 是返回值类型，用于指定 Lambda表达式的返回值类型，可以省略，表示由编译器根据函数体推导，
也可以使用 -> 符号显式指定，还可以在 c++14 中使用 auto 关键字来实现泛型返回值。
    4. function body 是函数体，用于表示 Lambda表达式的具体逻辑，可以是一条语句，也可以是多条语句，还可以在 c++14 中使用 constexpr 来实现编译期计算。
*/
//connect(信号发送者，信号，信号接收者，响应函数，连接类型)
//connect(信号发送者，信号，[=](){响应函数主体}，连接类型

//这里的MainWindow是在mainwindow.h中使用Q_OBJECT宏并继承于QMainWindow的MainWindow类
MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    /*  IMPORTANCE
    setupUi(this)
    其类似于构造函数，用于初始化GUI界面
    但在使用时需要注意的是，它最好放在MainWindow函数的第一句，先由该函数对图形化界面进行初始化，该过程可能附带着一系列内存分配操作
    若将其放在最后一句，可能会出现内存泄漏的情况（网友探雷）
    对于该函数，它主要是调用ui_mainwindow.h中定义的实现代码，而ui_mainwindow.h一般是整个项目代码编写完成后，编译时自动生成的
    因此setupUi(this)初始化的主界面样式多为编译器默认，初次编译后就可以在ui_mainwindow.h中进行修改
    */
    ui->setupUi(this);

    /*
    QPoint(left_distance, top_distance);   //以左上角点为坐标原点
    QSize(width, height);
    */
    west = new QPushButton(this);
    west->setText("West");
    west->setGeometry(QRect(QPoint(500, 430), QSize(100, 100)));
    /*  官方文档
    [static] QMetaObject::Connection QObject::connect(
        const QObject *sender,
        const char *signal,
        const QObject *receiver,
        const char *method,
        Qt::ConnectionType type = Qt::AutoConnection
    )；
    信号与槽的连接，可传入五个参数，最后一个可省略
    1. 信号发送者，一般为声明的Qt组件
    2. 发送信号，即组件对应的事件响应时产生的信号
    3. 信号接收者，直接由MainWindow自己接收
    4. 响应函数，由组件对应的槽函数（响应函数）接受信号并作出处理
    5. 连接类型，一般默认即可
    */
    connect(west, SIGNAL(clicked()), this, SLOT(on_pushButton_clicked_west()));

    east = new QPushButton(this);
    east->setText("East");
    east->setGeometry(QRect(QPoint(700, 430), QSize(100, 100)));
    connect(east, SIGNAL(clicked()), this, SLOT(on_pushButton_clicked_east()));

    north = new QPushButton(this);
    north->setText("North");
    north->setGeometry(QRect(QPoint(600, 430), QSize(100, 50)));
    connect(north, SIGNAL(clicked()), this, SLOT(on_pushButton_clicked_north()));

    south = new QPushButton(this);
    south->setText("South");
    south->setGeometry(QRect(QPoint(600, 480), QSize(100, 50)));
    connect(south,SIGNAL(clicked()), this, SLOT(on_pushButton_clicked_south()));

    teleport = new QPushButton(this);
    teleport->setText("Teleport");
    teleport->setGeometry(QRect(QPoint(500, 530), QSize(300, 50)));
    connect(teleport, SIGNAL(clicked()), this, SLOT(on_pushButton_clicked_teleport()));

    map = new QPushButton(this);
    map->setText("Map");
    map->setGeometry(QRect(QPoint(500, 580), QSize(300, 50)));
    connect(map, SIGNAL(clicked()), this, SLOT(on_pushButton_clicked_map()));
}

/*
引入程序主体，由其主函数实例化一个对象，并以此为运行主体
且后面将其作为程序与GUI组件建立连接的桥梁，更偏向于程序一方的对象
*/
ZorkUL temp;

//析构函数，当主窗口被销毁时调用，释放其占用的内存
MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::on_pushButton_clicked_west()
{
    interaction("west");
    // string w=temp.goWindowRoom("west");
    //
    // QString qstr = QString::fromStdString(w);
    // ui->textEdit->append(qstr);
}

void MainWindow::on_pushButton_clicked_north()
{
    interaction("north");
    // string n=temp.goWindowRoom("north");
    // QString qstr = QString::fromStdString(n);
    // ui->textEdit->append(qstr);
}

void MainWindow::on_pushButton_clicked_south()
{
    interaction("south");
    // string s=temp.goWindowRoom("south");
    // QString qstr = QString::fromStdString(s);
    // ui->textEdit->append(qstr);
}

void MainWindow::on_pushButton_clicked_east()
{
    interaction("east");
    // string str = "";
    // Room* nextRoom = temp.currentRoom->nextRoom("east");
    // Judge* judge = new Judge(temp.player, nextRoom->getMonster(), temp.currentRoom, nextRoom);
    // monster_interaction(judge);

    // if(judge->getMoveCheck()){
    //     string e = "";
    //     e += temp.goWindowRoom("east");
    //     QString qstr = QString::fromStdString(e);
    //     ui->textEdit->append(qstr);
    // }
    // else{
    //     string e = "";
    //     e += "[Info] Monster in Room [" + judge->getNextRoom()->shortDescription() + "] is alive, you can't enter this room.\n";
    //     e += temp.showMap();
    //     e += judge->getMonsterDescription();
    //     e += judge->getCharacterDescription();
    //     QString qstr = QString::fromStdString(e);
    //     ui->textEdit->append(qstr);
    // }
}

void MainWindow::on_pushButton_clicked_teleport()
{
    string str = temp.teleport()->longDescription();
    QString r = QString::fromStdString(str);
    ui->textEdit->append(r);
}

void MainWindow::on_pushButton_clicked_map(){
    string str = temp.showMap();
    QString qstr = QString::fromStdString(str);
    ui->textEdit->append(qstr);
}

void MainWindow::interaction(string direction){

    string str = "";
    Room* nextRoom = temp.currentRoom->nextRoom(direction);

    //判断前进方向是否存在房间
    if(nextRoom == NULL){
        str = "[Warning] Hit the wall!";
        //将程序中返回的字符串通过Qt组件自带的函数，应用合适且统一的编码方式，转换为可以在组件上打印的字符串
        QString qstr = QString::fromStdString(str);
        ui->textEdit->append(qstr);
        return ;
    }

    Judge* judge = new Judge(temp.player, nextRoom->getMonster(), temp.currentRoom, nextRoom);

    //判断下一房间是否为怪物房间，若是则进入 怪物-人物互动环节     在这一环节对moveCheck状态位进行矫正
    if(judge->getNextRoom()->getIsMonsterRoom() == true){
        monsterRoomDialog* dialog = new monsterRoomDialog(this);
        dialog->setJudge(judge);
        dialog->setModal(true);
        int state = dialog->exec();
        if(state == -1){
            str += "[Error] You must make a choice to continue the game instead closing the dialog.";
            QString qstr = QString::fromStdString(str);
            ui->textEdit->append(qstr);
            return ;
        }
    }
    int game = gameover(judge);

    //若game == -1 则表示游戏可以继续进行
    if(game == -1){
        //判断是否可以进入到下一房间，若可以则进入到下一房间，否则人物停留在原房间并打印相关提示   (可以移动 && 下一房间无怪物)
        if(judge->getMoveCheck() == true && judge->getNextRoom()->getIsMonsterRoom() == false){
            // judge--;
            // --judge;
            judge->staminaCost();
            str += temp.goWindowRoom(direction);
            QString qstr = QString::fromStdString(str);
            ui->textEdit->append(qstr);
            // judge->referee();
        }
        else{
            str += "[Failure] Monster in Room [" + judge->getNextRoom()->shortDescription() + "] is alive, you can't enter this room.\n";
            str += temp.showMap();
            str += judge->getMonsterDescription();
            str += judge->getCharacterDescription();
            QString qstr = QString::fromStdString(str);
            ui->textEdit->append(qstr);
        }
    }
    // delete judge;
}

int MainWindow::gameover(Judge* judge){
    int box = judge->getWinOrLost();
    if(box == 0 || box == 1 || box == 2){
        gameoverDialog* dialog = new gameoverDialog(this);
        dialog->setJudge(judge);
        dialog->setModal(true);
        dialog->exec();
        buttonsBaned();
    }
    return judge->getWinOrLost();
}

void MainWindow::buttonsBaned(){
    this->east->setEnabled(false);
    this->west->setEnabled(false);
    this->north->setEnabled(false);
    this->south->setEnabled(false);
    this->teleport->setEnabled(false);
    this->map->setEnabled(false);
}
