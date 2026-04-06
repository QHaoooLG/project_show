package com.sdut.cfg;

import org.springframework.web.servlet.HandlerInterceptor;

//登陆拦截器
public class LoginInterceptor implements HandlerInterceptor {
//    @Override
//    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object obj) throws Exception {
//        System.out.println(request.getRequestURI());
//        //若网页发来的请求中获取的会话中用户为空，即为未登陆状态，则会跳转回登陆页面并返回false
//        if (request.getSession().getAttribute("user") == null) {
//            response.sendRedirect("/login.html");
//            return false;
//        }
//        return HandlerInterceptor.super.preHandle(request, response, obj);
//    }
}
