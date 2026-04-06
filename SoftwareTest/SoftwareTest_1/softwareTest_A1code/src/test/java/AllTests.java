import Searches.*;
import Sorts.*;

import org.junit.platform.suite.api.SelectClasses;
import org.junit.platform.suite.api.Suite;

@Suite
@SelectClasses({SearchTests.class, SortTests.class})
public class AllTests {

}

