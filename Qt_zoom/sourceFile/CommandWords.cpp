#include "CommandWords.h"

vector<string> CommandWords::validCommands;

/**
 * Constructor - initialise the command words.
 * 初始化指令word
 */
CommandWords::CommandWords()
{
	// Populate the vector if we haven't already.
	// 如果还未填充矢量
	if (validCommands.empty())
	{
		validCommands.push_back("go");
		validCommands.push_back("quit");
		validCommands.push_back("info");
		validCommands.push_back("map");
		validCommands.push_back("take");
		validCommands.push_back("put");
		validCommands.push_back("teleports");
	}
}

/**
 * Check whether a given String is a valid command word.
 * Return true if it is, false if it isn't.
 * 检查给定的字符串是否是有效的命令字。如果是，则返回true，如果不是，则返回false。
 **/
bool CommandWords::isCommand(string aString)
{
	for (unsigned int i = 0; i < validCommands.size(); i++)
	{
		if (validCommands[i].compare(aString) == 0)
			return true;
	}
	// if we get here, the string was not found in the commands
	// 如歌到这没有检测到与之对应的有效字符串，认为给定的字符串是无效的返回false
	return false;
}

/*
 * Print all valid commands to System.out.
 打印所有的指令并输出
 */
void CommandWords::showAll()
{
	// Loops through validCommands and prints each to the screen.
	for (unsigned int i = 0; i < validCommands.size(); i++)
	{
		cout << validCommands[i] << "  ";
	}
	cout << endl;
}
