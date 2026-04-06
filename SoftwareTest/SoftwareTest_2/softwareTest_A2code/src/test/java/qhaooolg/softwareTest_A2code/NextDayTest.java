package qhaooolg.softwareTest_A2code;

import static org.junit.Assert.*;

import java.util.stream.Stream;
import java.lang.reflect.Method;
import java.util.*;
import java.util.concurrent.CopyOnWriteArrayList;

import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.NullAndEmptySource;

/*
 * *** Task ***
 * 1. Boundary Value Analysis
 * 2. Robustness Testing
 * 3. Worst-Case
 * 4. Robust Worst Case
 * 5. Strong Normal Equivalence Class Testing
 * 6. Strong Robust Equivalence Class Testing
 * 
 * */

/*
 * *** Assignment of Test ***
 * 
 * **************************************************************************************************************************
 * [Warning] This TestClass is based on Junit 5, please run it with Junit 5 !!! Or the compiler can't find test with Junit 4.
 * **************************************************************************************************************************
 * 
 * Range of valid input data:
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
 * y_max = 2012, y_min = 1812
 * m_max = 12, m_min = 1
 * d_max = 31, d_min = 1
 * 
 * */

/*
 * assertEquals(String message, object expected, object actual)
 * * Parameter 1 -> (optional) information printed as expected data mismatching actual data
 * */

public class NextDayTest {
	private NextDay_tested test = new NextDay_tested();	//测试函数 method received should be tested
	private NextDay expected = new NextDay();	//期望值函数 written by myself
	//in NextDayTest()
	static private Random_ num = new Random_();	//基于输入数据的范围随机生成测试用例
	/* public int random(); //method in Random_
	 * Function: generate a number which range is [min, max)
	 * */
	static private EquivalenceClass_nextDay ec = new EquivalenceClass_nextDay();	
	//generate equivalence class (packaged)
	static private BoundaryValue_nextDay bv = new BoundaryValue_nextDay();
	//generate data set about boundary test
		
	static int cnt = 1;
	
	NextDayTest(){
	}
	
	@BeforeEach
	public void setUp() throws Exception {
		String s = "";
		s += "*** Test Case " + cnt++ + " ***";
		System.out.println(s);
	}
	
	@AfterEach
	public void endUp() throws Exception {
	
	}
	
	/* *** Boundary Value Analysis *** 
	 * the number of test cases needed: 4n+1 = 4*3+1 = 13
	 * the species of data: nom, max, min, max-, min+
	 * strategy: single fault
	 * */
	@ParameterizedTest
	@MethodSource("BoundaryValueAnalysis_params")
	public synchronized void testInterface_BoundaryValueAnalysis(int y, int m, int d){	//各类数据测试接口
		System.out.println("(Boundary Value Analysis)");
		String s = "[Input Data] Year: " + y + ", Month: " + m + ", Day: " + d;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.nextDay(y, m, d), 
				test.nextDay(y, m, d));
	}
	static synchronized Stream<Arguments> BoundaryValueAnalysis_params() throws InterruptedException{
		bv.initialization_BoundaryValueAnalysis_params();
		List<Arguments> arglist = new ArrayList<>();
		
		arglist.add(Arguments.of(bv.y_nom(), bv.m_nom(), bv.d_nom()));
		for(int i=0; i<bv.y.size(); i++) {
			int y = bv.y.get(i);
			arglist.add(Arguments.of(y, bv.m_nom(), bv.d_nom()));
			Thread.sleep(1);	
			//每生成一个测试样例需要进行短时停滞，以避免程序运行过快导致其中几组测试样例的随机生成器所应用的系统时间种子无差别，从而没有达到真随机效果
		}
		for(int i=0; i<bv.m.size(); i++) {
			int m = bv.m.get(i);
			arglist.add(Arguments.of(bv.y_nom(), m, bv.d_nom()));
			Thread.sleep(1);	
		}
		for(int i=0; i<bv.d.size(); i++) {
			int d = bv.d.get(i);
			arglist.add(Arguments.of(bv.y_nom(), bv.m_nom(), d));
			Thread.sleep(1);	
		}
		return arglist.stream();
	}
	
	/* *** Robustness Testing *** 
	 * the number of test cases needed: 6n+1 = 6*3+1 = 19
	 * the species of data: nom, max, min, max-, min+, max+, min-
	 * strategy: single fault
	 * */
	@ParameterizedTest
	@MethodSource("RobustnessTesting_params")
	public synchronized void testInterface_RobustnessTesting(int y, int m, int d) {	//各类数据测试接口
		System.out.println("(Robustness Testing)");
		String s = "[Input Data] Year: " + y + ", Month: " + m + ", Day: " + d;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.nextDay(y, m, d), 
				test.nextDay(y, m, d));
	}
	static synchronized Stream<Arguments> RobustnessTesting_params() throws InterruptedException{
		bv.initialization_RobustnessTesting_params();
		List<Arguments> arglist = new ArrayList<>();
		
		arglist.add(Arguments.of(bv.y_nom(), bv.m_nom(), bv.d_nom()));
		for(int i=0; i<bv.y.size(); i++) {
			int y = bv.y.get(i);
			arglist.add(Arguments.of(y, bv.m_nom(), bv.d_nom()));
			Thread.sleep(1);	
		}
		for(int i=0; i<bv.m.size(); i++) {
			int m = bv.m.get(i);
			arglist.add(Arguments.of(bv.y_nom(), m, bv.d_nom()));
			Thread.sleep(1);	
		}
		for(int i=0; i<bv.d.size(); i++) {
			int d = bv.d.get(i);
			arglist.add(Arguments.of(bv.y_nom(), bv.m_nom(), d));
			Thread.sleep(1);	
		}
		return arglist.stream();
	}
	
	/* *** Worst Case *** 
	 * the number of test cases needed: 5^n = 5^3 = 125
	 * the species of data: nom, max, min, max-, min+
	 * strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("WorstCase_params")
	public synchronized void testInterface_WorstCase(int y, int m, int d) {	//各类数据测试接口
		System.out.println("(Worst Case)");
		String s = "[Input Data] Year: " + y + ", Month: " + m + ", Day: " + d;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.nextDay(y, m, d), 
				test.nextDay(y, m, d));
	}
	static synchronized Stream<Arguments> WorstCase_params(){
		bv.initialization_WorstCase_params();
		List<Arguments> arglist = new ArrayList<>();
		
		for(int i=0; i<bv.y.size(); i++) {
			for(int j=0; j<bv.m.size(); j++) {
				for(int k=0; k<bv.d.size(); k++) {
					arglist.add(Arguments.of(bv.y.get(i), bv.m.get(j), bv.d.get(k)) );
				}
			}
		}
		return arglist.stream();
	}
	
	/* *** Robust Worst Case *** 
	 * the number of test cases needed: 7^n = 7^3 = 343
	 * the species of data: nom, max, min, max-, min+, max+, min-
	 * strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("RobustWorstCase_params")
	public synchronized void testInterface_RobustWorstCase(int y, int m, int d) {	//各类数据测试接口
		System.out.println("(Robust Worst Case)");
		String s = "[Input Data] Year: " + y + ", Month: " + m + ", Day: " + d;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.nextDay(y, m, d), 
				test.nextDay(y, m, d));
	}
	static synchronized Stream<Arguments> RobustWorstCase_params(){
		bv.initialization_RobustWorstCase_params();
		List<Arguments> arglist = new ArrayList<>();
		
		for(int i=0; i<bv.y.size(); i++) {
			for(int j=0; j<bv.m.size(); j++) {
				for(int k=0; k<bv.d.size(); k++) {
					arglist.add(Arguments.of(bv.y.get(i), bv.m.get(j), bv.d.get(k)) );
				}
			}
		}
		return arglist.stream();
	}

	/* *** Strong Normal Equivalence Class Testing *** 
	 * the number of test cases needed: y*m*d = 2*3*4 = 24
	 * (y/m/d is the number of equivalence classes in corresponding dimension)
	 * the species of data: nom / max- / min+
	 * strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("StrongNormalEquivalenceClassTesting_params")
	public synchronized void testInterface_StrongNormalEquivalenceClassTesting(int y, int m, int d) {	//各类数据测试接口
		System.out.println("(Strong Normal Equivalence Class Testing)");
		String s = "[Input Data] Year: " + y + ", Month: " + m + ", Day: " + d;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.nextDay(y, m, d), 
				test.nextDay(y, m, d));
	}
	static synchronized Stream<Arguments> StrongNormalEquivalenceClassTesting_params() throws NoSuchMethodException, SecurityException, InterruptedException{
		ec.initialization_StrongNormalEquivalenceClassTesting_params();
		List<Arguments> arglist = new ArrayList<>();
		
		for(int i=0; i<ec.y.size(); i++)
			for(int j=0; j<ec.m.size(); j++)
				for(int k=0; k<ec.d.size(); k++)
					arglist.add(Arguments.of(ec.y.get(i), ec.m.get(j), ec.d.get(k)) );
		
		return arglist.stream();
	}
	
	/* *** Strong Robust Equivalence Class Testing *** 
	 * The number of test cases needed: (as followed)
	 * y*m*d + n_invalid_set + (n-1)_invalid_set_&1_valid_set + ... + 1_invalid_set&(n-1)_valid_set		or
	 * (y+2)*(m+2)*(d+2) = (2+2)*(3+2)*(4+2) = 4*5*6 = 120
	 * (y/m/d is the number of equivalence classes in corresponding dimension)
	 * The species of data: nom / max- / min+, max+, min-
	 * Strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("StrongRobustEquivalenceClassTesting_params")
	public void testInterface_StrongRobustEquivalenceClassTesting(int y, int m, int d) {	//各类数据测试接口
		System.out.println("(Strong Robust Equivalence Class Testing)");
		String s = "[Input Data] Year: " + y + ", Month: " + m + ", Day: " + d;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.nextDay(y, m, d), 
				test.nextDay(y, m, d));
	}
	static Stream<Arguments> StrongRobustEquivalenceClassTesting_params() throws InterruptedException{
		ec.initialization_StrongRobustEquivalenceClassTesting_params();
		List<Arguments> arglist = new ArrayList<>();
		
		for(int i=0; i<ec.y.size(); i++)
			for(int j=0; j<ec.m.size(); j++)
				for(int k=0; k<ec.d.size(); k++)
					arglist.add(Arguments.of(ec.y.get(i), ec.m.get(j), ec.d.get(k)) );
		
		return arglist.stream();
	}

	
	
}
