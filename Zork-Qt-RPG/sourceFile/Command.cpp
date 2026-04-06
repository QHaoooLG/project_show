#include "Command.h"

/**
 * Create a command object. First and second word must be supplied, but
 * either one (or both) can be null. The command word should be null to
 * indicate that this was a command that is not recognised by this game.
 * * 创建命令对象。必须提供第一个和第二个单词， 但其中一个（或两个）可以为空命令字应为null，表示这是一个本游戏无法识别的命令
 */
Command::Command(string firstWord, string secondWord)
{
	this->commandWord = firstWord;
	this->secondWord = secondWord;
}

/**
 * Return the command word (the first word) of this command. If the
 * command was not understood, the result is null.
 * 返回此命令的命令字（第一个字）。如果未理解该命令，则结果为null。
 */
string Command::getCommandWord()
{
	return this->commandWord;
}

/**
 * Return the second word of this command. Returns null if there was no
 * second word.
 */
string Command::getSecondWord()
{
	return this->secondWord;
}

/**
 * Return true if this command was not understood.
 * 如果得到的word无法识别则返回true
 * empty()函数如果是bool类型，若结果为NULL则返回空
 */
bool Command::isUnknown()
{
	return (commandWord.empty());
}

/**
 * Return true if the command has a second word.
 * 检测second word能否被识别，如果能被识别则返回false
 */
bool Command::hasSecondWord()
{
	return (!secondWord.empty());
}
