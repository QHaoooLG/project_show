package qhaooolg.softwareTest_A2code;

import java.util.*;

/*
 * Random.nextInt(a)	//生成[0, a)之间的随机整数
 * %tN Date类型对象转换为对应格式字符串
 * */

public class Random_ {
	Random num;
	
	//generate a number which range is [min, max)
	public int random(int min, int max) {
		int seed = Integer.parseInt(String.format("%tN", new Date()));
		num = new Random(seed);
		return min + num.nextInt(max - min);
	}
}

