package qhaooolg.softwareTest_A2code;

import java.util.Scanner;

public class Volume_tested{

    public static String volume(int length, int width, int height) {
        
		if (length<2||length>100||width<5||width>200||height<20||height>80){
            return "InputError";
        }
		String v = Integer.toString(length*width*height);
		return v;
    }

    public static void main(String[] args) {
//        System.out.println(volume(3, 10, 30));
//        System.out.println(volume(1, 10, 30));
        Scanner cn=new Scanner(System.in);
        System.out.println(volume(cn.nextInt(),cn.nextInt(),cn.nextInt()));
        cn.close();
    }
}
