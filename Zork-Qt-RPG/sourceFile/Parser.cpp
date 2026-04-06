#include "Parser.h"

Parser::Parser()
{
	commands = new CommandWords();
}

Command *Parser::getCommand()
{
	string inputLine = ""; // will hold the full input line
	string word1;		   // 将保持完整的输入行
	string word2;
	string buffer;
	vector<string> words;

	cout << "> "; // print prompt
				  // 打印提示

	getline(cin, buffer, '\n'); // read a line from cin to "buffer"
								// 从cin到“buffer”读取一行

	string::size_type pos = 0, last_pos = 0;

	// Break "buffer" up by spaces
	// 按空格分隔“缓冲区”

	bool finished = false;
	while (!finished)
	{
		pos = buffer.find_first_of(' ', last_pos);	  // find and remember first space.
		if (pos == string::npos)					  // 找到并记住第一个空格
		{											  // if we found the last word,如果找到找后一个单词
			words.push_back(buffer.substr(last_pos)); // add it to vector "words"加到vector “words”上

			finished = true; // and finish searching.结束检查
		}
		else
		{ // otherwise add to vector and move on to next word.否则，添加到向量并继续下一个单词

			words.push_back(buffer.substr(last_pos, pos - last_pos));
			last_pos = pos + 1;
		}
	}

	if (words.size() == 1) // was only 1 word entered?
		word1 = words[0];  // get first word
	else if (words.size() >= 2)
	{					  // were at least 2 words entered?
		word1 = words[0]; // get first word
		word2 = words[1]; // get second word
	}

	// note: we just ignore the rest of the input line.我们只是忽略输入行的其余部分
	// Now check whether this word is known. If so, create a command with it.现在检查这个词是否为人所知。如果是，请使用它创建一个命令
	// If not, create a "nil" command (empty string for unknown command).如果没有，请创建一个“nil”命令（未知命令为空字符串）

	if (commands->isCommand(word1))
		return new Command(word1, word2);
	else
		return new Command("", word2);
}

/**
 * Print out a list of valid command words.
 */
void Parser::showCommands()
{
	commands->showAll();
}
