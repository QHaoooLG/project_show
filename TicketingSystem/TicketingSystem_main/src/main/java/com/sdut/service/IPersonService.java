package com.sdut.service;

import com.sdut.pojo.Person;
import com.baomidou.mybatisplus.extension.service.IService;
import com.sdut.pojo.User;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import org.springframework.web.bind.annotation.RequestBody;

/**
 * <p>
 *  服务类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
public interface IPersonService extends IService<Person> {

    PageResult initPersons(String user_id, QueryPageBean queryPageBean);
}
