package com.sdut.controller;


import com.sdut.pojo.Tickets;
import com.sdut.service.ITicketsService;
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
@RequestMapping("/tickets")
public class TicketsController {

    @Resource
    private ITicketsService ticketsService;

    @RequestMapping("findPageInfo")
    public PageResult findPageInfo(@RequestBody QueryPageBean queryPageBean) {
        PageResult pageResult = ticketsService.findPageInfo(queryPageBean);
        return pageResult;
    }

    @RequestMapping("saveGroupInfo")
    public Result saveGroupInfo(@RequestBody Tickets tickets) {
        Result result = ticketsService.saveGroupInfo(tickets);
        return result;
    }

    @RequestMapping("deleteInfoById")
    public Result deleteInfoById(String id) {
        Result result = ticketsService.deleteInfoById(id);
        return result;
    }

    @RequestMapping("updateGroupInfo")
    public Result updateGroupInfo(@RequestBody Tickets tickets) {
        Result result = ticketsService.updateGroupInfo(tickets);
        return result;
    }
}