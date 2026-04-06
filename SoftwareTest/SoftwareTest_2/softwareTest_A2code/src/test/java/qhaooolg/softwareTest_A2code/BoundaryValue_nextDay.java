package qhaooolg.softwareTest_A2code;

import java.util.ArrayList;

public class BoundaryValue_nextDay {
	Random_ num = new Random_();
	
	static int y_min = 1812, y_max = 2012;
	static int m_min = 1, m_max = 12;
	static int d_min = 1, d_max = 31;
	static ArrayList<Integer> y, m, d;
	
	protected int y_nom() {
		int y = num.random(1812, 2013);
		return y;
	}
	
	protected int m_nom() {
		int y = num.random(1, 13);
		return y;
	}
	
	protected int d_nom() {
		int d = num.random(1, 32);
		return d;
	}
	
	//Boundary Value Analysis
	protected void initialization_BoundaryValueAnalysis_params() {
		y = new ArrayList<>();
		m = new ArrayList<>();
		d = new ArrayList<>();
		for(int i=0; i<2; i++) {
			y.add(y_min + i);
			y.add(y_max - i);
			m.add(m_min + i);
			m.add(m_max - i);
			d.add(d_min + i);
			d.add(d_max - i);
		}
	}
	
	//Robustness Testing
	protected void initialization_RobustnessTesting_params() {
		y = new ArrayList<>();
		m = new ArrayList<>();
		d = new ArrayList<>();
		for(int i=0; i<3; i++) {
			y.add(y_min - 1 + i);
			y.add(y_max + 1 - i);
			m.add(m_min - 1 + i);
			m.add(m_max + 1 - i);
			d.add(d_min - 1 + i);
			d.add(d_max + 1 - i);
		}
	}
	
	//Worst Case
	protected void initialization_WorstCase_params() {
		y = new ArrayList<>();
		m = new ArrayList<>();
		d = new ArrayList<>();
		y.add(this.y_nom());
		m.add(this.m_nom());
		d.add(this.d_nom());
		for(int i=0; i<2; i++) {
			y.add(y_min + i);
			y.add(y_max - i);
			m.add(m_min + i);
			m.add(m_max - i);
			d.add(d_min + i);
			d.add(d_max - i);
		}
	}
	
	//Robust Worst Case
	protected void initialization_RobustWorstCase_params() {
		y = new ArrayList<>();
		m = new ArrayList<>();
		d = new ArrayList<>();
		y.add(this.y_nom());
		m.add(this.m_nom());
		d.add(this.d_nom());
		for(int i=0; i<3; i++) {
			y.add(y_min - 1 + i);
			y.add(y_max + 1 - i);
			m.add(m_min - 1 + i);
			m.add(m_max + 1 - i);
			d.add(d_min - 1 + i);
			d.add(d_max + 1 - i);
		}
	}
}
