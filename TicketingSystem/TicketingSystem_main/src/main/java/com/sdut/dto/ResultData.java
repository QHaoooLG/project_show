package com.sdut.dto;

import lombok.Data;

@Data
public class ResultData {   //查询结果的数据类型

    private int status;
    private String msg;
    private Object data;

    public ResultData(int status) {
        this.status = status;
    }

    public ResultData(int status, String msg) {
        this.status = status;
        this.msg = msg;
    }
}
