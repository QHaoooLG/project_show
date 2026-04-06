package com.sdut.service;

import com.sdut.pojo.Sceneries;
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
public interface ISceneriesService extends IService<Sceneries> {

    PageResult findPageInfo(QueryPageBean queryPageBean);

    Result saveGroupInfo(Sceneries sceneries);

    Result deleteInfoById(String id);

    Result updateGroupInfo(Sceneries tickets);

    Result getPics();

    Result getAllScneries();

}
