package Searches;

import static org.junit.Assert.*;

import org.junit.Rule;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.rules.ExpectedException;

public class BinarySearchTest {
	private BinarySearch bs = new BinarySearch();
	
	@BeforeEach
	void setUp() throws Exception {
	}

	//使用多个以@Test为注解的测试样例，可以保证其中一个测试样例抛出异常时，其他样例依旧可以正常测试，效果等同于try...catch
	
	Integer [] test1 = {2,4,6,8,10};//第一次进else，median+1，第二次进if返回-1
	Integer [] test2 = {1,3,5};//第一次进else-if，median-1，第二次进if返回median
	Integer [] test8 = {1, 3, 4, 6, 8, 9, 11};
	//statement、branch coverage
	@Test
	public void testBinarySearch_normal_statementCoverage(){	//正常测试样例1
		 bs.find(test1, 1);
		 bs.find(test2, 1);
		 bs.find(test8, 7);
	}
	
	//basis coverage
	Integer [] test3 = null;//不可执行覆盖，进入方法find()后，必进方法search()
	Integer [] test4 = {1, 3, 4, 6, 8, 9, 11};//直接实现if返回-1
	Integer [] test5 = {1, 3, 6, 8, 9};//直接实现if返回median
	Integer [] test6 = {2,4,6,8,10,12,14};//第一次实现else-if，第二次实现if返回median
	Integer [] test7 = {1, 3, 4, 6, 8, 9, 11};//第一次执行else，第二次实现if返回median
	@Test
	public void testBinarySearch_normal_basisCoverage(){	//正常测试样例2
		 bs.search(test4,6,3,2);//如果使用方法find（）无法实现100%覆盖，仅能使用方法search（）
		 bs.find(test5,6);
		 bs.find(test6,1);
		 bs.search(test7,12,0,6);//如果使用方法find（）无法实现100%覆盖，仅能使用方法search（）
	}
	
	@Test
	public void testBinarySearch_fault(){	//异常测试，直接传入空数组和空值，获取异常
		//asserThrows用于获取预期异常，需要先指定异常类型，然后在后续调用的函数中获取，最终得到异常信息
		assertThrows(Exception.class, ()->bs.find(test3, null));	
	}
	
}
