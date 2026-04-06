#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv); //定义一个Qt应用程序对象，其构造函数接收的参数与main()相同  可看作Qt图形界面程序的入口
    MainWindow w;
    w.show();

    /*
    进入 Qt 应用程序的事件循环函数等待用户操作和系统的消息然后进行处理
    普通函数都是直接return 0;退出程序，而GUI程序通常需要与用户进行交互，不能自动关闭，需等待用户自行关闭
    所以最后返回的是等待用户点击窗口关闭按钮的值，当窗口被关闭时，整个程序才会结束，返回值一般为0
    */
    return a.exec();
}
