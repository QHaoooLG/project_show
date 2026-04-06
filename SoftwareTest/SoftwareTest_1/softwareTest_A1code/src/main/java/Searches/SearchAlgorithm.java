package Searches;

/**
 * The common interface of most searching algorithms
 * 查询算法的通用接口（需要每个算法都实现该接口来统一标准）
 *
 * @author Podshivalov Nikita (https://github.com/nikitap492)
 **/
public interface SearchAlgorithm {

    /**
     * @param key   is an element which should be found
     * @param array is an array where the element should be found
     * @param <T>   Comparable type
     * @return first found index of the element		返回值一般为目标值的在数组中的下标
     */
    <T extends Comparable<T>> int find(T array[], T key);	//使其子类必须实现find()
    //<T extends Comparable<T>> 是Java泛型的一部分，定义了一个类型参数T，它必须是一个实现了Comparable<T>接口的类
    //tip:这里传入find的数组类型必须为引用数据类型 -> T继承了Comparable<T>表明其必须是一个可以进行比较的对象，属于引用类型的范畴，而基本数据属于数据而非对象

    //测试时只需要引入对应包，如Search包，然后实例化对应查找类，向实例化的对象中对应查找算法传入预期测试样例
}
