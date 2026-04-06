package com.sdut;

import com.baomidou.mybatisplus.annotation.DbType;
import com.baomidou.mybatisplus.generator.AutoGenerator;
import com.baomidou.mybatisplus.generator.config.*;
import com.baomidou.mybatisplus.generator.config.rules.NamingStrategy;

public class LombokGenerator {
    public static void main(String[] args) {
        AutoGenerator autoGenerator = new AutoGenerator();  //自动生成器
        GlobalConfig globalConfig = new GlobalConfig(); //全局配置对象

        //全局配置参数
        globalConfig.setOpen(true);
        globalConfig.setAuthor("QHaoooLG");
        //代码生成路径
        globalConfig.setOutputDir("F:\\CodingBox\\IntelliJ_IDEA_workspace\\Database_ClassDesign\\Resource\\code_slice\\pojo_generation");
        globalConfig.setFileOverride(true); //路径覆盖设置
        autoGenerator.setGlobalConfig(globalConfig);

        // 数据源配置(根据自己数据的连接条件)
        DataSourceConfig dsc = new DataSourceConfig();
        dsc.setUrl("jdbc:mysql://localhost:3307/ticketing_classdesign");
        dsc.setDriverName("com.mysql.cj.jdbc.Driver");
        dsc.setUsername("root");
        dsc.setPassword("root");
        dsc.setDbType(DbType.MYSQL);
        autoGenerator.setDataSource(dsc);

        // 包配置
        PackageConfig pc = new PackageConfig();
        pc.setParent("com.sdut");
        pc.setController("controller");
        pc.setEntity("pojo");
        pc.setMapper("mapper");
        pc.setService("service");
        pc.setServiceImpl("impl");
        autoGenerator.setPackageInfo(pc);

        TemplateConfig templateConfig = new TemplateConfig();   //临时配置
        //设置临时配置中的服务接口ServiceImpl以及服务Service不生成
//        templateConfig.setServiceImpl(null);
//        templateConfig.setService(null);
        //将上述设置加入自动生成器中
        autoGenerator.setTemplate(templateConfig);

        StrategyConfig strategyConfig = new StrategyConfig();
        //数据库表映射到实体的命名策略
        strategyConfig.setNaming(NamingStrategy.underline_to_camel);
        //数据库表字段映射到实体的命名策略
        strategyConfig.setColumnNaming(NamingStrategy.underline_to_camel);
        strategyConfig.setEntityLombokModel(true);// lombok 模型
        strategyConfig.setRestControllerStyle(true); //restful api风格控制器

        String tableNames=
                "bookings,list_person,list_ticket,loads,pays,person,rebates,relation_booking,sceneries,tickets,user";
        strategyConfig.setInclude(tableNames.split(","));

        autoGenerator.setStrategy(strategyConfig);

        //执行
        autoGenerator.execute();
    }
}
