package com.sdut.service;

import com.sdut.pojo.Bookings;
import com.baomidou.mybatisplus.extension.service.IService;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
public interface IBookingsService extends IService<Bookings> {

    PageResult findPageInfo(QueryPageBean queryPageBean);

    Result saveBookingInfo(Bookings bookings);

    Result deleteInfoById(String id);

    //更新景点信息
    Result updateGroupInfo(Bookings bookings);
}
