package com.sdut.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.sdut.pojo.Bookings;
import com.sdut.mapper.BookingsMapper;
import com.sdut.pojo.Sceneries;
import com.sdut.service.IBookingsService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
@Service
public class BookingsServiceImpl extends ServiceImpl<BookingsMapper, Bookings> implements IBookingsService {

    @Resource
    private BookingsMapper bookingsMapper;

    @Override
    public PageResult findPageInfo(QueryPageBean queryPageBean) {
        //判断是否携带模糊查询的条件     条件查询->lambdaQueryWrapper
        String queryString = queryPageBean.getQueryString();
        LambdaQueryWrapper<Bookings> lambdaQueryWrapper = null;
        if(queryString != null && queryString.length() > 0){
            lambdaQueryWrapper = new LambdaQueryWrapper<>();
            lambdaQueryWrapper.like(Bookings::getId, queryString);
            lambdaQueryWrapper.or();
            lambdaQueryWrapper.like(Bookings::getTicketId, queryString);
            lambdaQueryWrapper.or();
            lambdaQueryWrapper.like(Bookings::getSceneryId, queryString);
            lambdaQueryWrapper.or();
            lambdaQueryWrapper.like(Bookings::getState, queryString);
        }

        //当前页 每页显示的条数
        Page<Bookings> page = new Page<>(queryPageBean.getCurrentPage(), queryPageBean.getPageSize());
        bookingsMapper.selectPage(page, lambdaQueryWrapper);
        return new PageResult(page.getTotal(), page.getRecords());
    }

    @Override
    public Result saveBookingInfo(Bookings bookings) {
        boolean flag = false;
        flag = bookingsMapper.insert(bookings) > 0;

        if(flag)
            return new Result(flag, "添加成功");
        else
            return new Result(flag, "添加失败");
    }

    @Override
    public Result deleteInfoById(String id) {
        boolean flag = true;
        LambdaQueryWrapper<Bookings> wrapper = new LambdaQueryWrapper<>();
        wrapper.eq(Bookings::getId, id);
        flag = bookingsMapper.deleteById(id) > 0;
        if(flag)
            return new Result(flag, "删除成功");
        else
            return new Result(flag, "删除失败");
    }

    @Override
    public Result updateGroupInfo(Bookings bookings) {
        boolean flag = false;
        flag = bookingsMapper.updateById(bookings) > 0;

        if(flag)
            return new Result(flag, "更新成功");
        else
            return new Result(flag, "更新失败");
    }

}
