#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

/*
...一般为用户在Qt中写好项目代码后由IDE自动生成ui_mainwindow.h文件
ui_mainwindow.h文件一般为编译后自动生成，但也可以手动添加到项目中
*/

//以下包含的功能包都是程序中用到的ui类型包
#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTextEdit>
#include <QtWidgets/QWidget>

/*
 * QT_BEGIN_NAMESPACE是在Qt_IDE环境下进行编译时编译器会自动包含的命名空间
 * 其作用是可以让同一份代码可以不经修改在Qt和非Qt两种环境下直接运行
*/
QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QTextEdit *textEdit;
    QMenuBar *menubar;
    QStatusBar *statuBar;


    /*
    QMainWindow是一个为用户提供主窗口程序的类，包含一个菜单栏（menu bar）、
    多个工具栏(tool bars)、多个锚接部件(dock widgets)、一个状态栏(status bar)及一个中心部件(central widget)
    */
    void setupUi(QMainWindow *MainWindow){
        if(MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(810, 700);   //窗口主界面尺寸(width, height)

        //QWidget类是所有用户界面对象的基类，主要用于界面显示
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        // centralwidget->setVisible(true);

        //textEdit是Qt中用于创建文本编辑器的类。它提供了一个可编辑的文本区域，可以用于输入和显示文本
        textEdit = new QTextEdit(centralwidget);
        textEdit->setObjectName("textEdit");
        //QRect(left_distance, top_distance, width, height)
        textEdit->setGeometry(QRect(10, 0, 480, 680));  //文本框位置及尺寸

        /*
        使用setCentralWidget()函数可以方便地设置窗口的中心部件，使其占据主要区域，并显示应用程序的主要内容
        setCentralWidget()函数会将之前设置的中心部件替换为新的中心部件
        如果之前已经设置了中心部件，调用setCentralWidget()函数会将之前的中心部件从窗口中移除
        */
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 800, 17));

        MainWindow->setMenuBar(menubar);
        statuBar = new QStatusBar(MainWindow);
        statuBar->setObjectName("statusbar");
        MainWindow->setStatusBar(statuBar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    //QTranslator类为文本输出提供国际化支持...
    //即为ui中的构件命名
    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
