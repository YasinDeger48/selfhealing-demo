package matrix;

@io.cucumber.testng.CucumberOptions(features = "classpath:features", glue = "matrix", plugin = "com.selfhealing.healer.cucumber.HealingCucumberPlugin")
public class RunCucumberTest extends io.cucumber.testng.AbstractTestNGCucumberTests {
}
