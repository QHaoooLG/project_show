package com.example.shoponline_android.utils;

public class Validators {
    private Validators() {
    }

    public static String validateUsername(String username) {
        if (username == null || username.trim().isEmpty()) {
            return "请输入用户名";
        }
        if (username.trim().length() < 3 || username.trim().length() > 20) {
            return "用户名长度需为 3-20 个字符";
        }
        return null;
    }

    public static String validatePassword(String password) {
        if (password == null || password.isEmpty()) {
            return "请输入密码";
        }
        if (password.length() < 6 || password.length() > 32) {
            return "密码长度需为 6-32 个字符";
        }
        return null;
    }

    public static String validateConfirmPassword(String password, String confirmPassword) {
        if (confirmPassword == null || confirmPassword.isEmpty()) {
            return "请再次输入密码";
        }
        if (!confirmPassword.equals(password)) {
            return "两次输入的密码不一致";
        }
        return null;
    }

    public static String validateProductName(String name) {
        if (name == null || name.trim().isEmpty()) {
            return "请输入商品名称";
        }
        if (name.trim().length() > 40) {
            return "商品名称不能超过 40 个字符";
        }
        return null;
    }

    public static String validatePrice(String priceText) {
        if (priceText == null || priceText.trim().isEmpty()) {
            return "请输入商品价格";
        }
        try {
            double price = Double.parseDouble(priceText.trim());
            if (price < 0) {
                return "商品价格不能为负数";
            }
            if (price > 999999.99) {
                return "商品价格不能超过 999999.99";
            }
        } catch (NumberFormatException e) {
            return "商品价格格式不正确";
        }
        return null;
    }

    public static double parsePrice(String priceText) {
        return Double.parseDouble(priceText.trim());
    }
}
