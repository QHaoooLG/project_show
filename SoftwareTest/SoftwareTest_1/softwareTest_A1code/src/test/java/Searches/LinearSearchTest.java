package Searches;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.*;

import org.junit.Rule;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.rules.ExpectedException;

class LinearSearchTest {
	private LinearSearch ls=new LinearSearch();

	@BeforeEach
	void setUp() throws Exception {
	}

	//statement、branch coverage
	Integer [] test1= {5, 3, 4, 6, 8};//直接执行至return i
	Integer [] test2= {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};//直接执行至return -1
	@Test
	public void testLinearSearch_normal_statementCoverage() {
		ls.find(test1, 5);
		ls.find(test2,11);
	}
	
	//basis coverage
	Integer [] test3= {5, 3, 4, 6, 8};//直接执行至return i
	Integer [] test4= {};//跳过for循环直接执行return -1
	Integer [] test5= {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};//直接执行至return -1
	@Test
	public void testLinearSearch_normal_basisCoverage() {
		ls.find(test3, 5);
		ls.find(test4, 1);
		ls.find(test5, 11);
	}
	
	@Test
	public void testLinearSearch_fault() {
		assertThrows(Exception.class,()->ls.find(test2,7));
	}

}
