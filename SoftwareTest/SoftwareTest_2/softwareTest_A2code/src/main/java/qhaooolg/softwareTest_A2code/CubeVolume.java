package qhaooolg.softwareTest_A2code;

import java.util.*;

public class CubeVolume {
		
	public String cubeVolume(int l, int w, int h) {	
		//length->[2, 100], width->[5, 200], height->[20, 80]
		try {
			//invalid input
			if(l < 2 || l > 100 || w < 5 || w > 200 || h < 20 || h > 80)
				throw new Exception();
			
			return output(l, w, h);
			
		}catch(Exception ex) {
			String exception_string = "InputError";
			return exception_string;
		}
	}
	
	private String output(int l, int w, int h) {
		int result = l * w * h;
//		String s = "[cube volume] " + result + "\n";
		String s = "";
		s += result;
		return s;
	}
	
	public static void main(String[] args) {

	}
}
