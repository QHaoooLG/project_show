package com.sdut.dto;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import lombok.Data;

@Data
public class SearchInfo {
    private String sea_val; //查询值
    private String sea_col; //查询列，当前为单列查询
    private String sea_relation;    //查询关系

    private Long page;  //Long为引用类型
    private Long limit;

    public Long getLimit() {     //设置每页数据上限，用于分页
        return limit == null ? 100000 : limit;
    }

    /*  下面一个方法代码块的函数头
    第一个<T> -> 表示该方法是泛型方法
    第二个<T> -> 即IPage<t>，表示该方法返回一个IPage<T>类型值
    第三个<T> -> 即Class<T>，为传入方法的参数，表示传入一个泛型类，意味着可以传递任何类型的类
     */
    public <T> IPage<T> getPageInfo(Class<T> cls) {
        if (page == null) return null;
        IPage<T> po = new Page<T>(page, limit);
        return po;
    }

    public <T> QueryWrapper<T> getQuery(Class<T> cls) {
        QueryWrapper<T> q = new QueryWrapper<T>();
        if (sea_val != null) {     //根据查询关系判断查询操作，可自行增删
            if (sea_relation == null) sea_relation = "=";
            if (sea_relation.equals("=")) q.eq(sea_col, sea_val);
            else if (sea_relation.equals("like")) q.like(sea_col, sea_val);
        }
        return q;
    }
}
