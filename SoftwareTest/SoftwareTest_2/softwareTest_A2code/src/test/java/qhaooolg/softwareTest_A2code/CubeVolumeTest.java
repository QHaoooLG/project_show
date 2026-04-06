package qhaooolg.softwareTest_A2code;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;

//* *** Task ***
//* 1. Boundary Value Analysis
//* 2. Robustness Testing
//* 3. Worst-Case
//* 4. Robust Worst Case
//* 5. Strong Normal Equivalence Class Testing
//* 6. Strong Robust Equivalence Class Testing
//* 
//* */

/*
* *** Assignment of Test ***
* 
* **************************************************************************************************************************
* [Warning] This TestClass is based on Junit 5, please run it with Junit 5 !!! Or the compiler can't find test with Junit 4.
* **************************************************************************************************************************
* 
* Range of valid input data:
* l->[2, 100] 
* w->[5, 200] 
* h->[20, 80]
* 
* To unify the default invalid data criteria, the range of invalid data is displayed as followed:
* l_overMin(l2)->[-100, 1] 	l_overMax(l3)->[101, 200]
* w_overMin(w2)->[-100, 4] 	w_overMax(w3)->[201, 300]
* h_overMin(h2)->[-100, 20] 	h_overMax(h3)->[81, 200]
* 
* Equivalence Class Partitioning:
* l1 = {length: 2...100}
* w1 = {width: 5...200}
* h1 = {height: 20...80}
* 
* l_max = 100, l_min = 2
* w_max = 200, w_min = 5
* h_max = 80, h_min = 20
* 
* */

/*
* assertEquals(String message, object expected, object actual)
* * Parameter 1 -> (optional) information printed as expected data mismatching actual data
* */


public class CubeVolumeTest {

	private Volume_tested test = new Volume_tested();	//测试函数 method received should be tested
	private CubeVolume expected = new CubeVolume();	//期望值函数 written by myself
	static private Random_ num = new Random_();	//基于输入数据的范围随机生成测试用例
	/* public int random(); //method in Random_
	 * Function: generate a number which range is [min, max)
	 * */
	static private EquivalenceClass_cubeVolume ec = new EquivalenceClass_cubeVolume();	
	//generate equivalence class (packaged)
	static private BoundaryValue_cubeVolume bv = new BoundaryValue_cubeVolume();
	//generate data set about boundary test
		
	static int cnt = 1;
	
	CubeVolumeTest(){
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
	 * the number of test cases needed: 4n+1
	 * the species of data: nom, max, min, max-, min+
	 * strategy: single fault
	 * */
	@ParameterizedTest
	@MethodSource("BoundaryValueAnalysis_params")
	public synchronized void testInterface_BoundaryValueAnalysis(int l, int w, int h){	//各类数据测试接口
		System.out.println("(Boundary Value Analysis)");
		String s = "[Input Data] Length: " + l + ", Width: " + w + ", Height: " + h;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.cubeVolume(l, w, h), 
				test.volume(l, w, h));
	}
	static synchronized Stream<Arguments> BoundaryValueAnalysis_params() throws InterruptedException{
		bv.initialization_BoundaryValueAnalysis_params();
		List<Arguments> arglist = new ArrayList<>();
		
		arglist.add(Arguments.of(bv.l_nom(), bv.w_nom(), bv.h_nom()));
		for(int i=0; i<bv.l.size(); i++) {
			int l = bv.l.get(i);
			arglist.add(Arguments.of(l, bv.w_nom(), bv.h_nom()));
			Thread.sleep(1);	
			//每生成一个测试样例需要进行短时停滞，以避免程序运行过快导致其中几组测试样例的随机生成器所应用的系统时间种子无差别，从而没有达到真随机效果
		}
		for(int i=0; i<bv.w.size(); i++) {
			int w = bv.w.get(i);
			arglist.add(Arguments.of(bv.l_nom(), w, bv.h_nom()));
			Thread.sleep(1);	
		}
		for(int i=0; i<bv.h.size(); i++) {
			int h = bv.h.get(i);
			arglist.add(Arguments.of(bv.l_nom(), bv.w_nom(), h));
			Thread.sleep(1);	
		}
		return arglist.stream();
	}
	
	/* *** Robustness Testing *** 
	 * the number of test cases needed: 6n+1
	 * the species of data: nom, max, min, max-, min+, max+, min-
	 * strategy: single fault
	 * */
	@ParameterizedTest
	@MethodSource("RobustnessTesting_params")
	public synchronized void testInterface_RobustnessTesting(int l, int w, int h) {	//各类数据测试接口
		System.out.println("(Robustness Testing)");
		String s = "[Input Data] Length: " + l + ", Width: " + w + ", Height: " + h;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.cubeVolume(l, w, h), 
				test.volume(l, w, h));
	}
	static synchronized Stream<Arguments> RobustnessTesting_params() throws InterruptedException{
		bv.initialization_RobustnessTesting_params();
		List<Arguments> arglist = new ArrayList<>();
		
		arglist.add(Arguments.of(bv.l_nom(), bv.w_nom(), bv.h_nom()));
		for(int i=0; i<bv.l.size(); i++) {
			int l = bv.l.get(i);
			arglist.add(Arguments.of(l, bv.w_nom(), bv.h_nom()));
			Thread.sleep(1);	
		}
		for(int i=0; i<bv.w.size(); i++) {
			int w = bv.w.get(i);
			arglist.add(Arguments.of(bv.l_nom(), w, bv.h_nom()));
			Thread.sleep(1);	
		}
		for(int i=0; i<bv.h.size(); i++) {
			int h = bv.h.get(i);
			arglist.add(Arguments.of(bv.l_nom(), bv.w_nom(), h));
			Thread.sleep(1);	
		}
		return arglist.stream();
	}
	
	/* *** Worst Case *** 
	 * the number of test cases needed: 5^n
	 * the species of data: nom, max, min, max-, min+
	 * strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("WorstCase_params")
	public synchronized void testInterface_WorstCase(int l, int w, int h) {	//各类数据测试接口
		System.out.println("(Worst Case)");
		String s = "[Input Data] Length: " + l + ", Width: " + w + ", Height: " + h;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.cubeVolume(l, w, h), 
				test.volume(l, w, h));
	}
	static synchronized Stream<Arguments> WorstCase_params(){
		bv.initialization_WorstCase_params();
		List<Arguments> arglist = new ArrayList<>();
		
		for(int i=0; i<bv.l.size(); i++) {
			for(int j=0; j<bv.w.size(); j++) {
				for(int k=0; k<bv.h.size(); k++) {
					arglist.add(Arguments.of(bv.l.get(i), bv.w.get(j), bv.h.get(k)) );
				}
			}
		}
		return arglist.stream();
	}
	
	/* *** Robust Worst Case *** 
	 * the number of test cases needed: 7^n
	 * the species of data: nom, max, min, max-, min+, max+, min-
	 * strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("RobustWorstCase_params")
	public synchronized void testInterface_RobustWorstCase(int l, int w, int h) {	//各类数据测试接口
		System.out.println("(Robust Worst Case)");
		String s = "[Input Data] Length: " + l + ", Width: " + w + ", Height: " + h;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.cubeVolume(l, w, h), 
				test.volume(l, w, h));
	}
	static synchronized Stream<Arguments> RobustWorstCase_params(){
		bv.initialization_RobustWorstCase_params();
		List<Arguments> arglist = new ArrayList<>();
		
		for(int i=0; i<bv.l.size(); i++) {
			for(int j=0; j<bv.w.size(); j++) {
				for(int k=0; k<bv.h.size(); k++) {
					arglist.add(Arguments.of(bv.l.get(i), bv.w.get(j), bv.h.get(k)) );
				}
			}
		}
		return arglist.stream();
	}
	
	/* *** Strong Normal Equivalence Class Testing *** 
	 * the number of test cases needed: l*w*h
	 * (l/w/h is the number of equivalence classes in corresponding dimension)
	 * the species of data: nom / max- / min+
	 * strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("StrongNormalEquivalenceClassTesting_params")
	public synchronized void testInterface_StrongNormalEquivalenceClassTesting(int l, int w, int h) {	//各类数据测试接口
		System.out.println("(Strong Normal Equivalence Class Testing)");
		String s = "[Input Data] Length: " + l + ", Width: " + w + ", Height: " + h;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.cubeVolume(l, w, h), 
				test.volume(l, w, h));
	}
	static synchronized Stream<Arguments> StrongNormalEquivalenceClassTesting_params() throws NoSuchMethodException, SecurityException, InterruptedException{
		ec.initialization_StrongNormalEquivalenceClassTesting_params();
		List<Arguments> arglist = new ArrayList<>();

		for(int i=0; i<ec.l.size(); i++)
			for(int j=0; j<ec.w.size(); j++)
				for(int k=0; k<ec.h.size(); k++)
					arglist.add(Arguments.of(ec.l.get(i), ec.w.get(j), ec.h.get(k)) );
		
		return arglist.stream();
	}
	
	/* *** Strong Robust Equivalence Class Testing *** 
	 * The number of test cases needed: (as followed)
	 * l*w*h + n_invalid_set + (n-1)_invalid_set_&1_valid_set + ... + 1_invalid_set&(n-1)_valid_set
	 * (l/w/h is the number of equivalence classes in corresponding dimension)
	 * The species of data: nom / max- / min+, max+, min-
	 * Strategy: multiple fault
	 * */
	@ParameterizedTest
	@MethodSource("StrongRobustEquivalenceClassTesting_params")
	public synchronized void testInterface_StrongRobustEquivalenceClassTesting(int l, int w, int h) {	//各类数据测试接口
		System.out.println("(Strong Robust Equivalence Class Testing)");
		String s = "[Input Data] Length: " + l + ", Width: " + w + ", Height: " + h;
		System.out.println(s);
		assertEquals("[WRONG INFORMATION] Data tested mismatching the expected data", 
				expected.cubeVolume(l, w, h), 
				test.volume(l, w, h));
	}
	static synchronized Stream<Arguments> StrongRobustEquivalenceClassTesting_params() throws NoSuchMethodException, SecurityException, InterruptedException{
		ec.initialization_StrongRobustEquivalenceClassTesting_params();
		List<Arguments> arglist = new ArrayList<>();

		for(int i=0; i<ec.l.size(); i++)
			for(int j=0; j<ec.w.size(); j++)
				for(int k=0; k<ec.h.size(); k++)
					arglist.add(Arguments.of(ec.l.get(i), ec.w.get(j), ec.h.get(k)) );
		
		return arglist.stream();
	}
}
