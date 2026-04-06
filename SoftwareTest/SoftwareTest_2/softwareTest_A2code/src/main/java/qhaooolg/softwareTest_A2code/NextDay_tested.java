package qhaooolg.softwareTest_A2code;

import java.util.Scanner;

public class NextDay_tested {
	public static String nextDay(int Year, int Month, int Day) {
		if (Year<1812||Year>2012||Month<1||Month>12||Day<1||Day>31) {
			System.out.println("InputError");
            return "InputError";
        }
		int[] Monthday = {31,28,31,30,31,30,31,31,30,31,30,31};
		if(Year%4==0&&Year%100!=0||Year%400==0)
			Monthday[1]=29;
		Day++;
        if (Day>Monthday[Month-1]) {
            Day=1;
            Month++;
        }
        if (Month>12) {
            Month=1;
            Year++;
        }
        String s = "";
        s += Year + " " + Month + " " + Day; 
        System.out.println(s);
		return Year+","+Month+","+Day;
	}
	
	public static void main(String[] args) {
//        System.out.println("The next day is:" +nextDay(1900,2,28));
//		NextDay_tested t = new NextDay_tested();
//		t.nextDay(2000, 1, 1);
//		t.nextDay(2000, 1, 31);
//		t.nextDay(2000, 2, 27);
//		t.nextDay(2000, 2, 28);
//		t.nextDay(2000, 2, 29);
//		t.nextDay(2000, 9, 30);
//		t.nextDay(2000, 12, 31);
//		t.nextDay(2001, 2, 27);
//		t.nextDay(2001, 2, 28);
//		t.nextDay(2001, 2, 29);
//		t.nextDay(1000, 1, 1);
//		t.nextDay(2001, 0, 1);
//		t.nextDay(2001, 2, 0);

//        Scanner cn=new Scanner(System.in);
//        System.out.println(nextDay(cn.nextInt(),cn.nextInt(),cn.nextInt()));
//        cn.close();
    }
}
