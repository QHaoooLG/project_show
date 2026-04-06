import java.util.Scanner;

public class NextDay {
	public static String nextDay(int Year, int Month, int Day) {
		if (Year<1812||Year>2012||Month<1||Month>12||Day<1||Day>31) {
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
		return Year+","+Month+","+Day;
	}
	
	public static void main(String[] args) {
//        System.out.println("The next day is:" +nextDay(1900,2,28));
        Scanner cn=new Scanner(System.in);
        System.out.println(nextDay(cn.nextInt(),cn.nextInt(),cn.nextInt()));
        cn.close();
    }
}
