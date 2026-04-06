#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QPushButton>
#include "monsterRoomDialog.h"
#include "gameoverDialog.h"

QT_BEGIN_NAMESPACE
//创建名为Ui的命名空间并在里面声明MainWindow类，与其他同名函数分隔，避免命名冲突
namespace Ui {
class MainWindow;
}
QT_END_NAMESPACE



class MainWindow : public QMainWindow{  //公开继承QMainWindow，创建一个自定义窗口类
    Q_OBJECT
/*
Q_OBJECT是一个宏，用于启用Qt的元对象系统，以支持：
信号与槽(Signals and Slots)机制、动态属性查找、对象间的通信等功能
使用了Q_OBJECT宏的类可以利用元对象系统中的功能，如定义信号和槽、实现动态属性、进行运行时类型信息查找等
该步操作是实现Qt提供的更多高级功能的关键步骤
*/

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();  //析构函数，当 函数调用结束后\对象被销毁时 自动调用，用于释放其占用的内存

    // bool eventFilter(QObject* obj, QEvent* event);  //MainWindow类的事件过滤器，用于玩家与怪物交互环节，判断鼠标点击事件是否基于Fight和Run两个按钮
    void interaction(string direction);
    int gameover(Judge* judge);
    void buttonsBaned();

/*
在私有槽中定义函数，它们都被声明为MainWindow类的私有成员函数，并用于响应不用的用户界面事件
在 Qt 中，通过将槽函数与特定的信号连接起来，可以实现在发生特定事件时执行相应的操作
槽函数一般的命名规则是 “$on_$信号源对象名_信号名” ，表示它是用于响应特定信号的函数
这里是定义五个按键的槽函数，以链接到其对应的事件函数
*/
private slots:
    void on_pushButton_clicked_west();
    void on_pushButton_clicked_north();
    void on_pushButton_clicked_south();
    void on_pushButton_clicked_east();
    void on_pushButton_clicked_teleport();
    void on_pushButton_clicked_map();

signals:
    // void fightOrRun(int);

private:
    Ui::MainWindow *ui; //UI实例指针
/*
通过这个指针，可以访问和操作 MainWindow 类的用户界面部分，包括其中的各种控件、布局等
这种设计模式通常被称为 “分离用户界面（Separate UI）”，它使得窗口类和用户界面部分能够分别管理和维护，提高了代码的可维护性和可扩展性
*/
    QPushButton *south, *west, *east, *north;
    QPushButton *teleport, *map;    //声明用于访问按键事件的指针

};
#endif // MAINWINDOW_H
