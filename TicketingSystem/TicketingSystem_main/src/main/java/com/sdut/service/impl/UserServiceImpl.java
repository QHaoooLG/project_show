package com.sdut.service.impl;

import com.baomidou.mybatisplus.core.conditions.query.LambdaQueryWrapper;
import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import com.sdut.dto.ResultData;
import com.sdut.pojo.Person;
import com.sdut.pojo.Sceneries;
import com.sdut.pojo.User;
import com.sdut.mapper.UserMapper;
import com.sdut.service.IUserService;
import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.sdut.util.PageResult;
import com.sdut.util.QueryPageBean;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import com.sdut.cfg.MD5;

import javax.annotation.Resource;
import javax.servlet.http.HttpSession;
import org.springframework.security.core.context.*;

import java.util.List;

/**
 * <p>
 *  服务实现类
 * </p>
 *
 * @author QHaoooLG
 * @since 2024-12-23
 */
@Service
public class UserServiceImpl extends ServiceImpl<UserMapper, User> implements IUserService {

    @Resource
    private UserMapper userMapper;

    @Override
    public ResultData login(User user, HttpSession session) {
        //参数中的user为登陆页面里键入用户名和密码的临时用户对象，用于从数据库中进行条件查询找实际用户以及核实密码
        System.out.println(user.getName());
        System.out.println(user.getPower());

        List<User> userList = userMapper.selectList(new QueryWrapper<User>()
                .eq("name", user.getName())
        );  //在数据库中根据用户名和删除标志进行查找，并将匹配的所有记录添加到userList中

        if (userList.size() != 1)    //条件查找到不止一个用户，表明用户名错误或其他情况
            return new ResultData(-1, "非法用户");
        User u = userList.get(0);   //获取userList中第一条记录(理论上应该只有一条记录，所有只获取第一条即可)

        String pass = MD5.getMD5(user.getPass());   //将获取的临时用户对象的密码转为MD5加密字段
        if (!u.getPass().equals(pass))  //比较实际用户和临时用户两者的密码是否匹配
            return new ResultData(-3, "密码错误");
        session.setMaxInactiveInterval(600); //设置会话有效时间，单位s
        //为当前登录用户状态设置为u
        session.setAttribute("user", u);    //将user属性设置为对应的实际用户对象，若无user属性则会先创建
        System.out.println("[Info] session attribute now set: " + u.getName());

        if(u.getPower().equals("admin"))
            return new ResultData(100, "管理员模式登陆成功");
        else
            return new ResultData(1, "登陆成功");
    }

    @Override
    public User getCurrentUser() {
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();

        if(authentication != null && authentication.getPrincipal() instanceof User)
            return (User) authentication.getPrincipal();    //当前登录用户
        else
            return null;    //用户未登录
    }


}
