package qhaooolg.softwareTest_A2code;

import java.sql.Time;
import java.util.*;

/* [Bug]
 * 2024/11/14
 * 
 * NORMAL TEST CASE
 * input:2001 2 29
 * output:InputError
 * 
 * WRONG TEST CASE
 * input:2001 11 31
 * output:2001 11 32
 * 
 * */

public class NextDay {
	
	int[] months = {-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};
	
	public String nextDay(int y, int m, int d) {
		try {
			
			//invalid input
			if(d < 1 || d > 31 || m < 1 || m > 12 || y < 1812 || y > 2012)
				throw new Exception();
			boolean leap = isLeapYear(y);	//count leap year
			
			//invalid input data with Feb against the rule
			if(m == 2)
				if(leap && d > 29 || !leap && d > 28)
					throw new Exception();
			
			//invalid input data without Feb against the rule
			if(m != 2 && d > months[m])
				throw new Exception();
			
			//judge function bodys
			if(leap) {
				if(m == 2)
					if(d == months[m]+1)
						return output(y, m+1, 1);
					else 
						return output(y, m, d+1);
				else 
					if(m == 12 && d == months[m])
						return output(y+1, 1, 1);
					else if(d == months[m])
						return output(y, m+1, 1);
					else 
						return output(y, m, d+1);
			}
			else {
				if(m == 12 && d == months[m])
					return output(y+1, 1, 1);
				else if(d == months[m])
					return output(y, m+1, 1);
				else 
					return output(y, m, d+1);
			}
			
		}catch(Exception ex) {
			String exception_string = "InputError";
			System.out.println(exception_string);
			return exception_string;
		}
	}
	
	public boolean isLeapYear(int y) {
		if(y % 4 == 0 && y % 100 != 0 || y % 400 == 0)
			return true;
		else 
			return false;
	}
	
	private String output(int y, int m, int d) {
//		String s = "[next day]Year:" + y + "\tMonth:" + m + "\tDay:" + d + "\n";
        String s = "";
        s += y + " " + m + " " + d; 
        String return_str = "";
		return_str += y + "," + m + "," + d;
		System.out.println(s);
		return return_str;
	}
	
	public static void main(String[] args) throws InterruptedException {
//		NextDay a = new NextDay();
//		
//		a.nextDay(2001, 2, 28);
//		a.nextDay(2001, 2, 29);
//		a.nextDay(2000, 2, 28);
//		a.nextDay(2000, 2, 29);
//		a.nextDay(1900, 2, 28);
//		a.nextDay(1900, 2, 29);
//		a.nextDay(1900, 11, 31);
//		a.nextDay(1900, 12, 32);
//		a.nextDay(1900, 11, 30);
//		a.nextDay(1900, 12, 31);

//		Random_ num = new Random_();
//		for(int i=0; i<100; i++) {
//			System.out.println(num.random(-100, 100));
//			Thread.sleep(1);
//		}
			
	}
}
