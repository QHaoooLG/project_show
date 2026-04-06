package com.sdut.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.sdut.mapper.ListTicketMapper;
import com.sdut.pojo.*;
import com.sdut.pojo.Tickets;
import com.sdut.pojo.Tickets;
import com.sdut.mapper.TicketsMapper;
import com.sdut.service.ITicketsService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sdut.util.MessageConstant;
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
public class TicketsServiceImpl extends ServiceImpl<TicketsMapper, Tickets> implements ITicketsService {

    @Resource
    private TicketsMapper ticketsMapper;
//    private ListTicketMapper listTicketMapper;

    @Override
    public PageResult findPageInfo(QueryPageBean queryPageBean) {
        //判断是否携带模糊查询的条件     条件查询->lambdaQueryWrapper
        String queryString = queryPageBean.getQueryString();
        LambdaQueryWrapper<Tickets> lambdaQueryWrapper = null;
        if(queryString != null && queryString.length() > 0){
            lambdaQueryWrapper = new LambdaQueryWrapper<>();
            lambdaQueryWrapper.like(Tickets::getId, queryString);
            lambdaQueryWrapper.or();
            lambdaQueryWrapper.like(Tickets::getText, queryString);
        }

        //当前页 每页显示的条数
        Page<Tickets> page = new Page<>(queryPageBean.getCurrentPage(), queryPageBean.getPageSize());
        ticketsMapper.selectPage(page, lambdaQueryWrapper);
        return new PageResult(page.getTotal(), page.getRecords());
    }

    @Override
    public Result saveGroupInfo(Tickets tickets) {
        boolean flag = false;
        //保存检查组信息
        flag = ticketsMapper.insert(tickets) > 0;

        if(flag)
            return new Result(flag, "添加成功");
        else
            return new Result(flag, "添加失败");
    }

    @Override
    public Result deleteInfoById(String id) {
        boolean flag = true;
        //删除该检查组对应的关系表(中间表)
        LambdaQueryWrapper<Tickets> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Tickets::getId, id);
//        flag = ticketsMapper.delete(wrapper) > 0;
        //删除检查组表中对应的记录
        flag = ticketsMapper.deleteById(id) > 0;
        if(flag)
            return new Result(flag, MessageConstant.DELETE_CHECKGROUP_SUCCESS);
        else
            return new Result(flag, MessageConstant.DELETE_CHECKGROUP_FAIL);
    }

    @Override
    public Result updateGroupInfo(Tickets tickets) {
        //更新检查组的数据
        boolean flag = false;
        flag = ticketsMapper.updateById(tickets) > 0;

        if(flag)
            return new Result(flag, "门票更新成功");
        else
            return new Result(flag, "门票更新失败");
    }
}
