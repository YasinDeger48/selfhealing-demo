package matrix;

@org.junit.runner.RunWith(io.cucumber.junit.Cucumber.class)
@io.cucumber.junit.CucumberOptions(features = "classpath:features", glue = "matrix", plugin = "com.selfhealing.healer.cucumber.HealingCucumberPlugin")
public class RunCucumberTest {
}
