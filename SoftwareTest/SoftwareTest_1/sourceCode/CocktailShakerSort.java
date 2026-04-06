package Sorts;

/**
 * @author Mateus Bizzo (https://github.com/MattBizzo)
 * @author Podshivalov Nikita (https://github.com/nikitap492)
 */

/*
 * 鸡尾酒排序：
 * 
 */
class CocktailShakerSort implements SortAlgorithm {

    /**
     * This method implements the Generic Cocktail Shaker Sort
     *
     * @param array The array to be sorted
     *              Sorts the array in increasing order
     **/

    @Override
    public <T extends Comparable<T>> T[] sort(T[] array) {

        int length = array.length;
        int left = 0;
        int right = length - 1;
        int swappedLeft, swappedRight;
        while (left < right) {	//每轮都可以找出一个max和min，并将排序范围不断缩小直至left=right，此时排序完成
            // front
            swappedRight = 0;
            for (int i = left; i < right; i++) {
                if (SortUtils.less(array[i + 1], array[i])) {
                	//遍历数组，按从小到大的顺序交换遍历到的数组元素，将当前最大的元素送到数组后排
                    SortUtils.swap(array, i, i + 1);
                    swappedRight = i;	//标记当前最大值下标的位置，往左遍历找当前最小值的指针从这里开始    标记交换后的数组最右侧下标
                }
            }
            // back
            right = swappedRight;	//以向右遍历的最后一个元素下标作为起点
            swappedLeft = length - 1;	//初始化为数组最右侧元素
            for (int j = right; j > left; j--) {	//向左遍历找最小值并交换
                if (SortUtils.less(array[j], array[j - 1])) {
                    SortUtils.swap(array, j - 1, j);
                    swappedLeft = j;	//标记已交换后的数组最左侧下标
                }
            }
            left = swappedLeft;	//下次遍历的左边界修正为标记最左下标
        }
        return array;

    }

    // Driver Program
    public static void main(String[] args) {
        // Integer Input
        Integer[] integers = {4, 23, 6, 78, 1, 54, 231, 9, 12};
        CocktailShakerSort shakerSort = new CocktailShakerSort();

        System.out.printf("[Cocktail Shaker Sort] ");
        // Output => 1 4 6 9 12 23 54 78 231
        SortUtils.print(shakerSort.sort(integers));

        System.out.printf("[Cocktail Shaker Sort] ");
        // String Input
        String[] strings = {"c", "a", "e", "b", "d"};
        SortUtils.print(shakerSort.sort(strings));
    }


}
