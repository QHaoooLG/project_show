package com.sdut.dto;

import lombok.Data;

import java.util.List;

@Data
public class ResultInfo {
    private int code;  //错误代码
    private String msg;    //错误信息，返回信息，需要返回传输成功与否的信息
    private long count;    //总行数
    private List data;  //本项目采用前端所要求的格式

    private String params;

}
