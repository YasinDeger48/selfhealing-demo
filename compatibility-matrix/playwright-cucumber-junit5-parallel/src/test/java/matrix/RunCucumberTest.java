package matrix;

@org.junit.platform.suite.api.Suite
@org.junit.platform.suite.api.IncludeEngines("cucumber")
@org.junit.platform.suite.api.SelectPackages("features")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.glue", value = "matrix")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.plugin", value = "com.selfhealing.healer.cucumber.HealingCucumberPlugin")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.execution.parallel.enabled", value = "true")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.execution.parallel.config.strategy", value = "fixed")
@org.junit.platform.suite.api.ConfigurationParameter(key = "cucumber.execution.parallel.config.fixed.parallelism", value = "3")
public class RunCucumberTest {
}
