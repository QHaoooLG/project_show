package com.sdut.cfg;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration  //说明是配置文件
public class AllConfig implements WebMvcConfigurer {
    //表明将该类插入到系统WebMvc相关设置中(重写覆盖)

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        //除了登陆时需要显示的内容需要显示，将其他所有内容进行拦截，
        registry.addInterceptor(new LoginInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns(
                        "/error",
                        "/loginstyle/**",
                        "/js/**",
                        "/img/**",
                        "/css/**",
                        "/layui/**",
                        "/login.html",
                        "/user/img_code",
                        "/user/repass.html",
                        "/static/css/**"
                );
        WebMvcConfigurer.super.addInterceptors(registry);
    }
}
