package com.sdut.controller;


import com.sdut.pojo.Bookings;
import com.sdut.pojo.Sceneries;
import com.sdut.service.IBookingsService;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-10
 */
@RestController
@RequestMapping("/bookings")
public class BookingsController {

    @Resource
    private IBookingsService bookingsService;

    @RequestMapping("findPageInfo")
    public PageResult findPageInfo(@RequestBody QueryPageBean queryPageBean){
        PageResult pageResult = bookingsService.findPageInfo(queryPageBean);
        return pageResult;
    }

    @RequestMapping("saveBookingInfo")
    public Result saveBookingInfo(@RequestBody Bookings bookings){
        Result result = bookingsService.saveBookingInfo(bookings);
        return result;
    }

    @RequestMapping("deleteInfoById")
    public Result deleteInfoById(String id){
        Result result = bookingsService.deleteInfoById(id);
        return result;
    }

    @RequestMapping("updateGroupInfo")
    public Result updateGroupInfo(@RequestBody Bookings bookings){
        Result result = bookingsService.updateGroupInfo(bookings);
        return result;
    }

}

