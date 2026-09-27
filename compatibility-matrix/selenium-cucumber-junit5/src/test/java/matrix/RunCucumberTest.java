package matrix;

@org.junit.platform.suite.api.Suite
@org.junit.platform.suite.api.IncludeEngines("cucumber")
@org.junit.platform.suite.api.SelectPackages("features")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.glue", value = "matrix")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.plugin", value = "com.selfhealing.healer.cucumber.HealingCucumberPlugin")
public class RunCucumberTest {
}
