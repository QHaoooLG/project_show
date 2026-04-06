package com.sdut.cfg;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.ResourceHandlerRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;


@Configuration
public class PicConfig implements WebMvcConfigurer {

    @Override
    public void addResourceHandlers(ResourceHandlerRegistry registry) {
        //将本地的文件夹加入服务器 相当于为本地文件夹创建一个服务器的地址映射，使其可以通过url访问，而非本地磁盘路径
        //url举例: localhost:8083/setpic_scenery/a.jpg        -> 指定本地存储文件夹后，url可用于测试路径是否正确
        //指定本地图片存储文件夹时，路径结束时要加盘符"/"
        registry.addResourceHandler("/setpic_scenery/**").addResourceLocations("file:F:/CodingBox/IntelliJ_IDEA_workspace/Database_ClassDesign/TicketingSystem_main/src/main/resources/static/img/sceneries/");
        registry.addResourceHandler("/img/**").addResourceLocations("file:F:/CodingBox/IntelliJ_IDEA_workspace/Database_ClassDesign/TicketingSystem_main/src/main/resources/static/img/");
        registry.addResourceHandler("/static/**").addResourceLocations("file:F:/CodingBox/IntelliJ_IDEA_workspace/Database_ClassDesign/TicketingSystem_main/src/main/resources/static/");
        registry.addResourceHandler("/public/**").addResourceLocations("file:F:/CodingBox/IntelliJ_IDEA_workspace/Database_ClassDesign/TicketingSystem_main/src/main/resources/public/");


    }
}
