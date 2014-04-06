# -- FILE: features/example.feature
Feature: Showing off behave

	Scenario: Run a simple test
		Given we have behave installed
		When we implement 5 tests
		Then behave will test them for us!

	Scenario Outline: Test with <thing>
		Given we have behave installed
		When we implement <result> tests
		Then behave will test it for us!

    Examples: Example_group
        | thing         | param | result | 
        | Red Tree Frog | mush  | 1 |
        | apples        | apple | 2 |

    Examples: Example 2
        | thing         | param | result |
        | iPhone        | toxic waste | 3  |
        | Galaxy Nexus  | toxic waste |  4 |