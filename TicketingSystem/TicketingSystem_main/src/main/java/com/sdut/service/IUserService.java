package com.sdut.service;

import com.sdut.dto.ResultData;
import com.sdut.pojo.User;
import com.baomidou.mybatisplus.extension.service.IService;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;

import javax.servlet.http.HttpSession;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
public interface IUserService extends IService<User> {

    ResultData login(User user, HttpSession session);

    public User getCurrentUser();
}
