package qhaooolg.softwareTest_A2code;

import java.util.ArrayList;

public class BoundaryValue_cubeVolume {
Random_ num = new Random_();
	
	static int l_min = 2, l_max = 100;
	static int w_min = 5, w_max = 200;
	static int h_min = 20, h_max = 80;
	static ArrayList<Integer> l, w, h;
	
	protected int l_nom() {
		int l = num.random(2, 101);
		return l;
	}
	
	protected int w_nom() {
		int w = num.random(5, 201);
		return w;
	}
	
	protected int h_nom() {
		int h = num.random(20, 81);
		return h;
	}
	
	//Boundary Value Analysis
	protected void initialization_BoundaryValueAnalysis_params() {
		l = new ArrayList<>();
		w = new ArrayList<>();
		h = new ArrayList<>();
		for(int i=0; i<2; i++) {
			l.add(l_min + i);
			l.add(l_max - i);
			w.add(w_min + i);
			w.add(w_max - i);
			h.add(h_min + i);
			h.add(h_max - i);
		}
	}
	
	//Robustness Testing
	protected void initialization_RobustnessTesting_params() {
		l = new ArrayList<>();
		w = new ArrayList<>();
		h = new ArrayList<>();
		for(int i=0; i<3; i++) {
			l.add(l_min - 1 + i);
			l.add(l_max + 1 - i);
			w.add(w_min - 1 + i);
			w.add(w_max + 1 - i);
			h.add(h_min - 1 + i);
			h.add(h_max + 1 - i);
		}
	}
	
	//Worst Case
	protected void initialization_WorstCase_params() {
		l = new ArrayList<>();
		w = new ArrayList<>();
		h = new ArrayList<>();
		l.add(this.l_nom());
		w.add(this.w_nom());
		h.add(this.h_nom());
		for(int i=0; i<2; i++) {
			l.add(l_min + i);
			l.add(l_max - i);
			w.add(w_min + i);
			w.add(w_max - i);
			h.add(h_min + i);
			h.add(h_max - i);
		}
	}
	
	//Robust Worst Case
	protected void initialization_RobustWorstCase_params() {
		l = new ArrayList<>();
		w = new ArrayList<>();
		h = new ArrayList<>();
		l.add(this.l_nom());
		w.add(this.w_nom());
		h.add(this.h_nom());
		for(int i=0; i<3; i++) {
			l.add(l_min - 1 + i);
			l.add(l_max + 1 - i);
			w.add(w_min - 1 + i);
			w.add(w_max + 1 - i);
			h.add(h_min - 1 + i);
			h.add(h_max + 1 - i);
		}
	}
}
