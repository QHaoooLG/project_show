package com.sdut.service;

import com.sdut.pojo.Tickets;
import com.baomidou.mybatisplus.extension.service.IService;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;
import org.springframework.web.bind.annotation.RequestBody;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
public interface ITicketsService extends IService<Tickets> {

    PageResult findPageInfo(QueryPageBean queryPageBean);

    Result saveGroupInfo(Tickets tickets);

    Result deleteInfoById(String id);

    Result updateGroupInfo(@RequestBody Tickets tickets);

}
