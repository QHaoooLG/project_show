package Sorts;

import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class CocktailShakerSortTest {
	private CocktailShakerSort css = new CocktailShakerSort();

	@BeforeEach
	void setUp() throws Exception {
	}
	
	Integer[] t1 = {2, 3, 0, 1};
 	@Test
	void test_normal_StatementCoverage() {	//正常测试-Statement Coverage
		css.sort(t1);
	}
	
	Integer[] tt1 = {3, 2, 1};	//两个if均只走true
	Integer[] tt2 = null;	//由于算法特性，无法做到两个if都只走一次false，故将其中一条路径拆分为下面两条路径
	Integer[] tt2_1 = {3, 2, 2};	//第一个if走一次true,第二个if走一次false
	Integer[] tt2_2 = {1, 2};	//第一个if走false,第二个for走false
	@Test
	void test_normal_BranchCoverage() {	//正常测试-Branch Coverage
		css.sort(tt1);
		//计算出的路径仅支持80% Branch Coverage
		css.sort(tt2_1);
		css.sort(tt2_2);
	}
	
	Integer[] ttt1 = {1};	//第一个while走false
	Integer[] ttt2 = null;	//第一个for->false,第二个for->false	算法不可达路径，当数组元素个数>=2时，一定会进入while并执行第一个for
	Integer[] ttt3 = {1, 2};	//第一个if->false, 第二个for->false
	Integer[] ttt4 = {2, 1};		//第一个if->true,第二个for->false
	Integer[] ttt5 = null;	//第一个for->false,第二个if->false	算法不可达路径
	Integer[] ttt6 = null;	//第一个for->false,第二个if->true	算法不可达路径
	Integer[] ttt_extra1 = {1, 2, 1};	//第二个if->false
	Integer[] ttt_extra2 = {3, 2, 1};	//第二个if->true
	@Test
	void test_normal_BasisPathsCoverage() {	//正常测试-Basis Paths Coverage
		css.sort(ttt1);
		css.sort(ttt3);
		css.sort(ttt4);	
//		//画出的Basis Paths仅支持到Complexity 66.7% Coverage
		css.sort(ttt_extra1);
		css.sort(ttt_extra2);
	}
	
	Integer[] test = {};
	@Test
	void test_exception() {	//异常测试
		assertThrows(Exception.class, ()->css.sort(test));
	}

}
