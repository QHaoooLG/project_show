package com.sdut.controller;


import com.sdut.cfg.MakeVerificationCode;
import com.sdut.dto.ResultData;
import com.sdut.mapper.UserMapper;
import com.sdut.pojo.User;
import com.sdut.service.IUserService;
import com.sdut.util.Result;
import org.springframework.boot.autoconfigure.neo4j.Neo4jProperties;
import org.springframework.boot.web.servlet.server.Session;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.web.bind.annotation.RestController;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-10
 */
@RestController
@RequestMapping("/user")
public class UserController {

    @Resource
    private IUserService userService;

    //用户登录
    @RequestMapping("login")
    public ResultData login(User user, String code, HttpSession session) throws Exception {
        String verify_code = session.getAttribute("checkcode").toString();
        if (!code.equals(verify_code))
            return new ResultData(-4, "验证码错误");
        return userService.login(user, session);
    }

    //验证码
    @RequestMapping("img_code")
    public void img(HttpServletResponse response, HttpSession session) throws Exception {
        response.setContentType("image/png");   //设置内容类型，需要让网页明白
        //从网页接收的servlet反应输出数据流通过验证码配置工具生成验证码字符串，将该字符串赋给code，期间会生成验证码图片并存入指定路径
        String code = MakeVerificationCode.getImg(response.getOutputStream());
        session.setAttribute("checkcode", code);
    }

    //用户登出
    @RequestMapping("outlogin")
    public void outlogin(HttpServletResponse response, HttpSession session) throws Exception {
        session.removeAttribute("user");
        response.sendRedirect("/login.html");
    }

    //获取当前登录的用户
    @RequestMapping("getLoginUser")
    public Result getLoginUser(HttpSession session) {
        // 获取当前登录用户
        User user = (User) session.getAttribute("user");
        System.out.println("[Info]/user/getLoginUser return " + user.getName());
        if(user != null)
            return new Result(true, "已登录", user);
        else
            return new Result(false, "未登录!!!");
    }

    @RequestMapping("getLoginUserId")
    public Result getLoginUserId(HttpSession session) {
        // 获取当前登录用户
        User user = (User) session.getAttribute("user");
        System.out.println("[Info]/user/getLoginUser return " + user.getName());

        if(user != null)
            return new Result(true, user.getId(), user);
        else
            return new Result(false, "未登录!!!");
    }

    //未生效
    @RequestMapping("getCurrentUser")
    public Result getCurrentUser(){
        User user = userService.getCurrentUser();
        System.out.println("[Info]/user/getCurrentUser return " + user.getName());

        if(user != null)
            return new Result(true, "已登录", user);
        else
            return new Result(false, "未登录!!!");
    }


}

