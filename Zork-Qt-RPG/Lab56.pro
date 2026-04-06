QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++17

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    sourceFile/Character.cpp \
    sourceFile/Command.cpp \
    sourceFile/CommandWords.cpp \
    sourceFile/Food.cpp \
    sourceFile/Judge.cpp \
    sourceFile/Monster.cpp \
    sourceFile/Parser.cpp \
    sourceFile/Room.cpp \
    sourceFile/Scholarism.cpp \
    sourceFile/Weapon.cpp \
    sourceFile/ZorkUL.cpp \
    sourceFile/gameoverDialog.cpp \
    sourceFile/item.cpp \
    sourceFile/main.cpp \
    sourceFile/mainwindow.cpp \
    sourceFile/monsterRoomDialog.cpp

HEADERS += \
    sourceFile/Character.h \
    sourceFile/Command.h \
    sourceFile/CommandWords.h \
    sourceFile/Food.h \
    sourceFile/Judge.h \
    sourceFile/Monster.h \
    sourceFile/Parser.h \
    sourceFile/Room.h \
    sourceFile/Scholarism.h \
    sourceFile/Weapon.h \
    sourceFile/ZorkUL.h \
    sourceFile/gameoverDialog.h \
    sourceFile/item.h \
    sourceFile/mainwindow.h \
    sourceFile/monsterRoomDialog.h \
    sourceFile/ui_mainwindow.h

FORMS += \
    sourceFile/mainwindow.ui

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
