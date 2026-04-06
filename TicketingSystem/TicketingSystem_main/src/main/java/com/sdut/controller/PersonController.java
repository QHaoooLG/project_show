package com.sdut.controller;


import com.sdut.pojo.User;
import com.sdut.service.IPersonService;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
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
@RequestMapping("/person")
public class PersonController {

    @Resource
    private IPersonService personService;

    @RequestMapping("initPersons")
    public PageResult initPersons( String user_id, @RequestBody QueryPageBean queryPageBean) {
        PageResult pageResult = personService.initPersons(user_id, queryPageBean);
        return pageResult;
    }

}

