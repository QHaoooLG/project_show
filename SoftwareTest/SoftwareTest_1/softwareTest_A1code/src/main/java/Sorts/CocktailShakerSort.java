package Sorts;

/**
 * @author Mateus Bizzo (https://github.com/MattBizzo)
 * @author Podshivalov Nikita (https://github.com/nikitap492)
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
        while (left < right) {
            // front -> find max
            swappedRight = 0;
            for (int i = left; i < right; i++) {	//找最大，从最右侧开始放
                if (SortUtils.less(array[i + 1], array[i])) {	//右边的数小于左边的数，则交换；否则直接将i赋为右数下标
                    SortUtils.swap(array, i, i + 1);
                    swappedRight = i;
                }
            }
            // back	-> find min
            right = swappedRight;
            swappedLeft = length - 1;
            for (int j = right; j > left; j--) {	//找最小，从最左侧开始放
                if (SortUtils.less(array[j], array[j - 1])) {	//
                    SortUtils.swap(array, j - 1, j);
                    swappedLeft = j;
                }
            }
            left = swappedLeft;
        }
        return array;

    }

    // Driver Program
    public static void main(String[] args) {
        // Integer Input
        Integer[] integers = {4, 23, 6, 78, 1, 54, 231, 9, 12};
        CocktailShakerSort shakerSort = new CocktailShakerSort();

        // Output => 1 4 6 9 12 23 54 78 231
        SortUtils.print(shakerSort.sort(integers));

        // String Input
        String[] strings = {"c", "a", "e", "b", "d"};
        SortUtils.print(shakerSort.sort(strings));
    }


}
