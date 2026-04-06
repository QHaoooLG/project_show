package Searches;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.*;

/*
 * statement coverage and branch coverage:
 * 1.34,35,46,47,51,53,55,57,63,64,46,47,48,35,36
 * 2.34,35,46,47,51,53,55,57,63,68,69,46,47,51,53,55,56,35,36
 * 3.34,35,46,47,51,53,55,57,63,68,74,46,47,51,53,55,,57,58,35,36
 * basis coverage:
 * 1.34,35,36不可覆盖
 * 2.34,35,46,47,48,35,36
 * 3.34,35,46,47,51,53,55,56,35,36
 * 4.34,35,46,47,51,53,55,57,58,35,36
 * 5.34,35,46,47,51,53,55,57,63,64,46,35,36
 * 6.34,35,46,47,51,53,55,57,63,68,69,46,35,36
 * 7.34,35,46,47,51,53,55,57,63,68,74,46,35,36
 */


import org.junit.Rule;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.rules.ExpectedException;

class TernarySearchTest {
	TernarySearch ts=new TernarySearch();
	
	@BeforeEach
	void setUp() throws Exception {
	}

	//statement 、branch coverage
	Integer [] test1 = {0,1,2,4,5};//第一次key值小于mid1,第二次start>end值
	Integer [] test2 = {0,1,2,3};//第一次key值大于mid2，第二次key=mid1
	Integer [] test3 = {1,2,3,4,5,6,7};//第一次属于else，第二次key=mid2
	@Test
	public void testTernarySearch_normal_statementCoverage() {
		ts.find(test1,-1);
		ts.find(test2, 3);
		ts.find(test3, 4);
	}

	//basis coverage
	Integer [] test4 = null;//不可实现，进入方法find（）后必须进方法ternarySearch（）
    Integer [] test5 = null;//第一次进入直接进if，返回-1
	Integer [] test6 = {0,1,2,3};//第一次进入key=array[mid1]
	Integer [] test7 = {0,1,2,3};//第一次进入key=array[mid2]
	Integer [] test8 = {0,1,2,4,5};//第一次key<array[mid1],第二次进入if返回-1
	Integer [] test9 = {1,2,3,4,5};//第一次key>array[mid2],第二次进入if返回-1
	Integer [] test10 = null;//第一次进入else，第二次无法进入if返回-1，除非进入else-if
	@Test
	public void testTernarySearch_normal_basisCoverage() {
		ts.find(test1,-1);
		ts.find(test2, 3);
		ts.find(test3, 4);
		ts.find(test6, 1);
		ts.find(test7, 2);
		ts.find(test8, -1);
		ts.find(test9, 6);
	}

	Integer [] test11= {};
	@Test
	public void testLinearSearch_fault() {
		assertThrows(Exception.class,()->ts.find(test2,10));
	}

}
