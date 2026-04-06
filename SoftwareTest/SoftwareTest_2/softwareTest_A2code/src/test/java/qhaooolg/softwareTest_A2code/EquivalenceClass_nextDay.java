package qhaooolg.softwareTest_A2code;

import java.lang.reflect.Method;
import java.util.ArrayList;

/* Range of valid input data:
 * y->[1812, 2012] 
 * m->[1, 12] 
 * d->[1, 31]
 * 
 * To unify the default invalid data criteria, the range of invalid data is displayed as followed:
 * y_overMin(y3)->[0, 1811] 	y_overMax(y4)->[2013, 3000]
 * m_overMin(m4)->[-100, 0] 	m_overMax(m5)->[13, 100]
 * d_overMin(d5)->[-100, 0] 	m_overMax(d6)->[32, 100]
 * 
 * Equivalence Class Partitioning:
 * y1 = {year: 1812...2012 | leap_year(year)}
 * y2 = {year: 1812...2012 | common_year(year)}
 * m1 = {month: 1...12 | days(month) = 30} = {4, 6, 9, 11}
 * m2 = {month: 1...12 | days(month) = 31} = {1, 3, 5, 7, 8, 10, 12}
 * m3 = {2}
 * d1 = {day: 1...28}
 * d2 = {day: 1...29}
 * d3 = {day: 1...30}
 * d4 = {day: 1...31}
 * 
 * */

public class EquivalenceClass_nextDay {
	Random_ num = new Random_();	//generate a number which range is [min, max)
	NextDay nextday = new NextDay();
	
	int[] m1 = {4, 6, 9, 11};
	int[] m2 = {1, 3, 5, 7, 8, 10, 12};
	static ArrayList<Integer> y, m, d;

	
	protected int y1() throws InterruptedException {
		int y = num.random(1812, 2013);
		while(!nextday.isLeapYear(y)) {
			y = num.random(1812, 2013);
			Thread.sleep(1);
		}
		return y;
	}
	
	protected int y2() throws InterruptedException {
		int y = num.random(1812, 2013);
		while(nextday.isLeapYear(y)) {
			y = num.random(1812, 2013);
			Thread.sleep(1);
		}
		return y;
	}
	
	protected int y3() {
		int y = num.random(0, 1812);
		return y;
	}
	
	protected int y4() {
		int y = num.random(2013, 3001);
		return y;
	}
	
/* ****************************************************** */
	
	protected int m1() throws InterruptedException {
		int i = num.random(0, 4);
		return m1[i];
	}
	
	protected int m2() throws InterruptedException {
		int i = num.random(0, 7);
		return m2[i];
	}
	
	protected int m3() {
		return 2;
	}
	
	protected int m4() {
		int y = num.random(-100, 1);
		return y;
	}
	
	protected int m5() {
		int y = num.random(13, 101);
		return y;
	}
	
/* *********************************** */	
	
	protected int d1() {
		int d = num.random(1, 29);
		return d;
	}
	
	protected int d2() {
		int d = num.random(1, 30);
		return d;
	}
	
	protected int d3() {
		int d = num.random(1, 31);
		return d;
	}
	
	protected int d4() {
		int d = num.random(1, 32);
		return d;
	}
	
	protected int d5() {
		int d = num.random(-100, 1);
		return d;
	}
	
	protected int d6() {
		int d = num.random(32, 101);
		return d;
	}
	
	protected void initialization_StrongNormalEquivalenceClassTesting_params() throws InterruptedException {
		y = new ArrayList<>();
		m = new ArrayList<>();
		d = new ArrayList<>();
		y.add(this.y1());
		y.add(this.y2());
		m.add(this.m1());
		m.add(this.m2());
		m.add(this.m3());
		d.add(this.d1());
		d.add(this.d2());
		d.add(this.d3());
		d.add(this.d4());
	}
	
	protected void initialization_StrongRobustEquivalenceClassTesting_params() throws InterruptedException{
		y = new ArrayList<>();
		m = new ArrayList<>();
		d = new ArrayList<>();
		y.add(this.y1());
		y.add(this.y2());
		y.add(this.y3());
		y.add(this.y4());
		m.add(this.m1());
		m.add(this.m2());
		m.add(this.m3());
		m.add(this.m4());
		m.add(this.m5());
		d.add(this.d1());
		d.add(this.d2());
		d.add(this.d3());
		d.add(this.d4());
		d.add(this.d5());
		d.add(this.d6());
	}
	
	public static void main(String[] args) throws InterruptedException {	//function test
		EquivalenceClass_nextDay o = new EquivalenceClass_nextDay();
		
//		for(int i=0; i<100; i++) {
//			int y1 = o.y1();
//			System.out.println(y1 % 4);
//			Thread.sleep(1);
//		}
//		for(int i=0; i<100; i++) {
//			int y2 = o.y2();
//			int result = y2 % 4;
//			String s = "";
//			s += y2 + " | " + result ; 
//			System.out.println(s);
//			Thread.sleep(1);
//		}
//		for(int i=0; i<100; i++) {
//			int m1 = o.m1();
//			System.out.println(m1);
//			Thread.sleep(1);
//		}
//		for(int i=0; i<100; i++) {
//			int m2 = o.m2();
//			System.out.println(m2);
//			Thread.sleep(1);
//		}
		for(int i=0; i<100; i++) {
			int d1 = o.d1();
			System.out.println(d1);
			Thread.sleep(1);
		}
	}
}
