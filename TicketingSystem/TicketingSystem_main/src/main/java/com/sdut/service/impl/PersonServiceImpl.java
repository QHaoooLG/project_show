package com.sdut.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.sdut.pojo.Person;
import com.sdut.mapper.PersonMapper;
import com.sdut.pojo.Sceneries;
import com.sdut.pojo.User;
import com.sdut.service.IPersonService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
@Service
public class PersonServiceImpl extends ServiceImpl<PersonMapper, Person> implements IPersonService {

    @Resource
    private PersonMapper personMapper;

    @Override
    public PageResult initPersons(String user_id, QueryPageBean queryPageBean) {
//        String user_id = user.getId();
        //判断是否携带模糊查询的条件     条件查询->lambdaQueryWrapper
        LambdaQueryWrapper<Person> lambdaQueryWrapper = new LambdaQueryWrapper<>();
        lambdaQueryWrapper.eq(Person::getId, user_id);

        //当前页 每页显示的条数
        Page<Person> page = new Page<>(queryPageBean.getCurrentPage(), queryPageBean.getPageSize());
        personMapper.selectPage(page, lambdaQueryWrapper);
        return new PageResult(page.getTotal(), page.getRecords());
    }
}
