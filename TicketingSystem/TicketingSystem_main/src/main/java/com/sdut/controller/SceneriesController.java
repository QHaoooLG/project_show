package com.sdut.controller;


import com.sdut.pojo.Sceneries;
import com.sdut.pojo.Tickets;
import com.sdut.service.ISceneriesService;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import com.sdut.util.Result;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;

import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import javax.annotation.Resource;
import java.io.File;
import java.io.IOException;
import java.util.UUID;

/**
 * <p>
 *  前端控制器
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-10
 */
@RestController
@RequestMapping("/sceneries")
public class SceneriesController {

    @Resource
    private ISceneriesService sceneriesService;

    @RequestMapping("findPageInfo")
    public PageResult findPageInfo(@RequestBody QueryPageBean queryPageBean){
        PageResult pageResult = sceneriesService.findPageInfo(queryPageBean);
        return pageResult;
    }

    @RequestMapping("saveGroupInfo")
    public Result saveGroupInfo(@RequestBody Sceneries sceneries){
        Result result = sceneriesService.saveGroupInfo(sceneries);
        return result;
    }

    @RequestMapping("deleteInfoById")
    public Result deleteInfoById(String id){
        Result result = sceneriesService.deleteInfoById(id);
        return result;
    }

    @RequestMapping("updateGroupInfo")
    public Result updateGroupInfo(@RequestBody Sceneries sceneries){
        Result result = sceneriesService.updateGroupInfo(sceneries);
        return result;
    }

    @RequestMapping("uploadFile")
    //方法传入参数中使用注解@RequestParam，会将传入参数变为后端完成请求的硬性要求，若未传输名为imgFile的文件则会报错
    public Result uploadFile(@RequestParam(name = "imgFile") MultipartFile imgfile) throws IOException {
        //获取图片存储位置
        String path = "F:\\CodingBox\\IntelliJ_IDEA_workspace\\Database_ClassDesign\\TicketingSystem_main\\src\\main\\resources\\static\\img\\sceneries\\";
        //获取图片的完整名，即名称加文件后缀名
        String originalFileName = imgfile.getOriginalFilename();
        //为图片重新命名
        int lastIndex = originalFileName.lastIndexOf(".");
        String substring = originalFileName.substring(lastIndex);   //获取图片的文件后缀名 .jpg
        String uuid = UUID.randomUUID().toString(); //随机生成字符串   7f824a3d-dfee-4143-bec7-493a62edf44b2
        String newPicName = uuid + substring;   //7f824a3d-dfee-4143-bec7-493a62edf44b2.jpg
        File file = new File(path + newPicName);    //指定图片重命名后的路径
        try {
            imgfile.transferTo(file);
        }catch (Exception ex){
            ex.printStackTrace();
        }

        return new Result(true, null, newPicName);
    }

    @RequestMapping("getPics")
    public Result getPics(){
        Result result = sceneriesService.getPics();
        return result;
    }

    @RequestMapping("getAllScneries")
    public Result getAllScneries(){
        Result result = sceneriesService.getAllScneries();
        return result;
    }
}

