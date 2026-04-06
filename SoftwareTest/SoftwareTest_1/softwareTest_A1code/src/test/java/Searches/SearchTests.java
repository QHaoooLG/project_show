package Searches;

import org.junit.platform.suite.api.SelectClasses;
import org.junit.platform.suite.api.Suite;

@Suite
@SelectClasses({ BinarySearchTest.class, LinearSearchTest.class ,TernarySearchTest.class})
public class SearchTests{

}

