package com.sdut.cfg;

import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.*;
import java.util.Random;

public class MakeVerificationCode {
    static Random random = new Random();
    //验证码宽高
    static int width = 100;
    static int height = 50;


    //获取随机颜色
    private static Color getRandomColor() {
        return new Color(random.nextInt(255), random.nextInt(255), random.nextInt(255));
    }

    //获取随机字符
    private static String getRandomString() {
        char[] StringLibrary = "0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM".toCharArray();//验证码字符字典
        int index;//随机坐标
        String showString = "";
        for (int i = 0; i < 4; i++) {//四个随机验证字符，四次循环
            index = random.nextInt(StringLibrary.length);
            showString += String.valueOf(StringLibrary[index]);
        }
        return showString;
    }

    //保存验证码为图片
    private static void saveCode(BufferedImage imageBuffer) {
        try {
            ImageIO.write(imageBuffer, "png", new FileOutputStream(new File("F:\\CodingBox\\IntelliJ_IDEA_workspace\\Database_ClassDesign\\TicketingSystem_main\\src\\main\\resources\\public\\user\\img_code\\imgcode.png")));//这里要将图片保存路径改成你的，建议用相对路径
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String getImg(OutputStream out) {
        BufferedImage imageBuffer = new BufferedImage(width, height, BufferedImage.TYPE_INT_RGB);
        Graphics g = init(imageBuffer);//得到画笔
        drawBackgroundPane(g);//画一个彩色背景
        String code = drawcode(g);//画验证字符
        drawLine(g);//画干扰线
        try {
            ImageIO.write(imageBuffer, "png", out);//这里要将图片保存路径改成你的，建议用相对路径
        } catch (Exception e) {
            e.printStackTrace();
        }
        return code;
    }

    //画干扰线
    private static void drawLine(Graphics g) {
        g.setColor(new Color(0, 0, 0));//黑色线
        for (int i = 0; i < 30; i++) {
            int x1 = random.nextInt(width);
            int x2 = random.nextInt(width);
            int y1 = random.nextInt(height);
            int y2 = random.nextInt(height);
            g.drawLine(x1, y1, x2, y2);
        }
    }

    // 初始化画笔
    private static Graphics init(BufferedImage imageBuffer) {
        // 获取画笔
        Graphics g = imageBuffer.getGraphics();// 获取画笔
        g.setFont(new Font(Font.MONOSPACED, Font.BOLD, 35));// 设置字体
        return g;
    }

    // 画彩色背景
    private static void drawBackgroundPane(Graphics g) {
        for (int i = 0; i < width; i++) {
            for (int j = 0; j < height; j++) {
                g.setColor(getRandomColor());//随机画笔颜色
                g.fillRect(i, j, 1, 1);
            }
        }
    }

    //画验证码字符
    private static String drawcode(Graphics g) {
        String code = getRandomString();
        g.setColor(new Color(0, 0, 0));//设置画笔颜色
        g.drawString(code, width / 10, height / 4 * 3);
        return code;
    }
}