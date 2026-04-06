package qhaooolg.softwareTest_A2code;

import java.util.ArrayList;

/* Range of valid input data:
* l->[2, 100] 
* w->[5, 200] 
* h->[20, 80]
* 
* To unify the default invalid data criteria, the range of invalid data is displayed as followed:
* l_overMin(l2)->[-100, 1] 	l_overMax(l3)->[101, 200]
* w_overMin(w2)->[-100, 4] 	w_overMax(w3)->[201, 300]
* h_overMin(h2)->[-100, 19] 	h_overMax(h3)->[81, 200]
* 
* Equivalence Class Partitioning:
* l1 = {length: 2...100}
* w1 = {width: 5...200}
* h1 = {height: 20...80}
* 
* */


public class EquivalenceClass_cubeVolume {
	Random_ num = new Random_();	//generate a number which range is [min, max)
	NextDay nextday = new NextDay();
	static ArrayList<Integer> l, w, h;
	
	protected int l1() throws InterruptedException {
		int l = num.random(2, 101);
		return l;
	}
	
	protected int l2() throws InterruptedException {
		int l = num.random(-100, 2);
		return l;
	}
	
	protected int l3() throws InterruptedException {
		int l = num.random(101, 201);
		return l;
	}
	
	/* ****************************************************** */
	protected int w1() throws InterruptedException {
		int w = num.random(5, 201);
		return w;
	}
	
	protected int w2() throws InterruptedException {
		int w = num.random(-100, 5);
		return w;
	}
	
	protected int w3() throws InterruptedException {
		int w = num.random(201, 301);
		return w;
	}
	
	/* ****************************************************** */
	protected int h1() throws InterruptedException {
		int h= num.random(20, 81);
		return h;
	}
	
	protected int h2() throws InterruptedException {
		int h = num.random(-100, 20);
		return h;
	}
	
	protected int h3() throws InterruptedException {
		int h = num.random(81, 201);
		return h;
	}
	
	
	protected void initialization_StrongNormalEquivalenceClassTesting_params() throws InterruptedException{
		l = new ArrayList<>();
		w = new ArrayList<>();
		h = new ArrayList<>();
		l.add(this.l1());
		w.add(this.w1());
		h.add(this.h1());
	}
	
	protected void initialization_StrongRobustEquivalenceClassTesting_params() throws InterruptedException{
		l = new ArrayList<>();
		w = new ArrayList<>();
		h = new ArrayList<>();
		l.add(this.l1());
		l.add(this.l2());
		l.add(this.l3());
		w.add(this.w1());
		w.add(this.w2());
		w.add(this.w3());
		h.add(this.h1());
		h.add(this.h2());
		h.add(this.h3());
	}

}
