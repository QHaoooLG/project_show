package com.sdut.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.sdut.pojo.Sceneries;
import com.sdut.mapper.SceneriesMapper;
import com.sdut.service.ISceneriesService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.util.ArrayList;
import java.util.List;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
@Service
public class SceneriesServiceImpl extends ServiceImpl<SceneriesMapper, Sceneries> implements ISceneriesService {

    @Resource
    private SceneriesMapper sceneriesMapper;

    @Override
    public PageResult findPageInfo(QueryPageBean queryPageBean) {
        //判断是否携带模糊查询的条件     条件查询->lambdaQueryWrapper
        String queryString = queryPageBean.getQueryString();
        LambdaQueryWrapper<Sceneries> lambdaQueryWrapper = null;
        if(queryString != null && queryString.length() > 0){
            lambdaQueryWrapper = new LambdaQueryWrapper<>();
            lambdaQueryWrapper.like(Sceneries::getId, queryString);
            lambdaQueryWrapper.or();
            lambdaQueryWrapper.like(Sceneries::getText, queryString);
            lambdaQueryWrapper.or();
            lambdaQueryWrapper.like(Sceneries::getName, queryString);
        }

        //当前页 每页显示的条数
        Page<Sceneries> page = new Page<>(queryPageBean.getCurrentPage(), queryPageBean.getPageSize());
        sceneriesMapper.selectPage(page, lambdaQueryWrapper);
        return new PageResult(page.getTotal(), page.getRecords());
    }

    //新建景点信息
    @Override
    public Result saveGroupInfo(Sceneries sceneries) {
        boolean flag = false;
        //保存检查组信息
        flag = sceneriesMapper.insert(sceneries) > 0;

        if(flag)
            return new Result(flag, "添加成功");
        else
            return new Result(flag, "添加失败");
    }

    //删除景点信息
    @Override
    public Result deleteInfoById(String id) {
        boolean flag = true;
        //删除该检查组对应的关系表(中间表)
        LambdaQueryWrapper<Sceneries> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Sceneries::getId, id);
        //删除检查组表中对应的记录
        flag = sceneriesMapper.deleteById(id) > 0;
        if(flag)
            return new Result(flag, "删除成功");
        else
            return new Result(flag, "删除失败");
    }

    //更新景点信息
    @Override
    public Result updateGroupInfo(Sceneries sceneries) {
        //更新检查组的数据
        boolean flag = false;
        flag = sceneriesMapper.updateById(sceneries) > 0;

        if(flag)
            return new Result(flag, "更新成功");
        else
            return new Result(flag, "更新失败");
    }

    @Override
    public Result getPics() {
        LambdaQueryWrapper<Sceneries> lambdaQueryWrapper = new LambdaQueryWrapper<>();
        lambdaQueryWrapper.eq(Sceneries::getName, "泰山");
        lambdaQueryWrapper.or().eq(Sceneries::getName, "张家界");
        lambdaQueryWrapper.or().eq(Sceneries::getName, "苏州园林");
        lambdaQueryWrapper.or().eq(Sceneries::getName, "呼伦贝尔大草原");

        List<Sceneries> list = sceneriesMapper.selectList(lambdaQueryWrapper);
        List<String> picList = new ArrayList<>();
        for(Sceneries sc : list){
            picList.add(sc.getImg());
        }

        //返回查找到的景点的照片文件名
        return new Result(true, null, picList);
    }

    @Override
    public Result getAllScneries() {
        List<Sceneries> list = sceneriesMapper.selectList(null);
        return new Result(true, null, list);
    }


}
