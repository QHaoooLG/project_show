package Sorts;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class MergeSortTest {
	private MergeSort ms = new MergeSort();

	@BeforeEach
	void setUp() throws Exception {
	}

	Integer[] t1 = null;	//merge()中的if->true		算法不可达，若该if结构只走一边，则后续补全另一分治的数组时一定不会执行if结构中走过的分支处理的数组
	Integer[] t2 = null;	//merge()中的if->false	算法不可达
	Integer[] t_extra1 = {1,1};	//merge()中if->true,第二个while->false,第三个while->true
	Integer[] t_extra2 = {2,1};	//merge()中if->false,第二个while->true,第三个while->false
	@Test
	void test_normal_StatementCoverage() {
		//计算出的路径均无法找到对应的实际测试样例
		ms.sort(t_extra1);
		ms.sort(t_extra2);
	}
	
	Integer[] tt1 = {};	//merge()中的if->true
	Integer[] tt2 = null;	//doSort()中只调用第一个doSort()然后第二次遇到if->false	算法不可达，doSort()中的三个函数属于并列关系，只能被全部调用或全不调用
	Integer[] tt3 = null;	//doSort()中调用前两个doSort()然后第二次遇到if->false	算法不可达
	Integer[] tt4 = {1,1};	//merge()中if->true,第二个while->false,第三个while->true
	Integer[] tt5 = {2,1};	//merge()中if->false,第二个while->true,第三个while->false
	@Test
	void test_normal_BranchCoverage() {
		ms.sort(tt1);
		ms.sort(tt4);
		ms.sort(tt5);
	}
	
	Integer[] ttt1 = null;	//只执行sort()	算法不可达，sort()中必定会调用doSort()
	Integer[] ttt2 = {};	//merge()中的if->true
	Integer[] ttt3 = null;	//doSort()中只有第一个doSort()调用两次		算法不可达
	Integer[] ttt4 = null;	//doSort()中前两个doSort()调用两次	算法不可达
	Integer[] ttt5 = null;	//doSort()中调用merge()而不进入merge()函数体	算法不可达
	Integer[] ttt6 = null;	//merge()中所有while->false	算法不可达
	Integer[] ttt7 = null;	//merge()中第一个while->true,if->false,后两个while->false	算法不可达，只要进入merge()便会有分组，一定会有未分配完的组
	Integer[] ttt8 = null;	//merge()中第一个while->true,if->true,后两个while->false		算法不可达
	Integer[] ttt9 = null;	//merge()中后两个while->false	算法不可达
	Integer[] ttt10 = null;	//merge()中后两个while->false	算法不可达
	Integer[] ttt_extra1 = {1,1};
	Integer[] ttt_extra2 = {2,1};
	@Test
	void test_normal_BasisPathsCoverage() {
		ms.sort(ttt2);
		//计算出的路径仅支持2/9 = 22.2% Complexity Coverage
		ms.sort(ttt_extra1);
		ms.sort(ttt_extra2);
	}
	
	Integer[] test = {};
	@Test
	void test_exception() {
		assertThrows(Exception.class, ()->ms.sort(test));
	}

}
