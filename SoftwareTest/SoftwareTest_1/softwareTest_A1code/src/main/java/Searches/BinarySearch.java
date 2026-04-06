package Searches;

import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.ThreadLocalRandom;
import java.util.stream.IntStream;

import static java.lang.String.format;

/**
 *
 *
 *	二分查找
 * Binary search is one of the most popular algorithms
 * The algorithm finds the position of a target value within a sorted array
 *	
 * Worst-case performance	O(log n)	最坏情况
 * Best-case performance	O(1)	最优情况	
 * Average performance	O(log n)	平均表现
 * Worst-case space complexity	O(1)	最坏情况下的空间复杂度
 *
 *
 * @author Varun Upadhyay (https://github.com/varunu28)
 * @author Podshivalov Nikita (https://github.com/nikitap492)
 *
 * @see SearchAlgorithm
 * @see IterativeBinarySearch
 *
 */

class BinarySearch implements SearchAlgorithm {

    /**
     *
     * @param array is an array where the element should be found
     * @param key is an element which should be found
     * @param <T> is any comparable type	任意可比较类型
     * @return index of the element		返回目标元素的下标
     */
	
	//提供一个相当于接口的函数头，可以有效减少调用函数时录入的参数量，增强封装特性
    @Override
    public  <T extends Comparable<T>> int find(T[] array, T key) {	
        return search(array, key, 0, array.length);
    }

    /**
     * This method implements the Generic Binary Search
     *
     * @param array The array to make the binary search
     * @param key The number you are looking for
     * @param left The lower bound
     * @param right The  upper bound
     * @return the location of the key
     **/
    
    //算法主体
    public <T extends Comparable<T>> int search(T array[], T key, int left, int right){
        if (right < left) return -1; // this means that the key not found

        // find median
        int median = (left + right) >>> 1;	//求下标的中位数
        // >>> 为无符号右移运算符，这里是将结果向右移动1位，在二进制中相当于除以2
        //与普通的除法不同，无符号右移会丢弃低位，并且用0填充高位，因此它是一个整数除法，不会产生小数部分
        int comp = key.compareTo(array[median]);	//时刻将key与中位数进行比较

        if (comp == 0) {	//若相等则输出中位数的下标
            return median;
        } else if (comp < 0) {	//key<中位数，则在数组左半部分进行查找
            return search(array, key, left, median - 1);
        } else {
            return search(array, key, median + 1, right);
        }
    }

    // Driver Program
    //自带的随机测试主函数
    public static void main(String[] args) {
        // Just generate data
        Random r = ThreadLocalRandom.current();

        int size = 100;	//数组元素个数为100
        int maxElement = 100000;	//元素最大值为100000

        //生成的随机数组为整型、有序的
        Integer[] integers = IntStream.generate(() -> r.nextInt(maxElement)).limit(size).sorted().boxed().toArray(Integer[]::new);


        // The element that should be found
        //随机生成下标，范围为[0,99]，将下标对应的数组元素赋给shouldBeFound
        int shouldBeFound = integers[r.nextInt(size - 1)];

        BinarySearch search = new BinarySearch();
        int atIndex = search.find(integers, shouldBeFound);	//传入随机生成的数组和目标数进行测试

        //输出自编写二分查找算法的测试情况
        System.out.println(format(	
            "[Binary Search] Should be found: %d. Found %d at index %d. An array length %d",
            shouldBeFound, integers[atIndex], atIndex, size
        ));

        //使用java自带的二分查找进行检查
        int toCheck = Arrays.binarySearch(integers, shouldBeFound);
        System.out.println(format("[Binary Search] Found by system method at an index: %d. Is equal: %b", toCheck, toCheck == atIndex));
    }
}
