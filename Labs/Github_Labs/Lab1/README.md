
This lab focuses on 5 modules, which includes creating a virtual environment, creating a GitHub repository, creating Python files, creating test files using pytest and unittest, and implementing GitHub Actions.




## Step 1: Creating a Virtual Environment

In software development, it's crucial to manage project dependencies and isolate your project's environment from the global Python environment. This isolation ensures that your project remains consistent, stable, and free from conflicts with other Python packages or projects. To achieve this, we create a virtual environment dedicated to our project. <br>
<br>
To create a virtual environment, follow these steps:

1. Open a Command Prompt or Terminal in the directory where you want to create your project.
2. Choose a name for your virtual environment (e.g "lab_01") and run the appropriate command:
    ```
    python -m venv lab_01
    ```
3. Activate the virtual environment
    ```
    lab01\Scripts\activate
    ```
    After activation, you will see the virtual environment's name in your command prompt or terminal, indicating that you are working within the virtual environment.
   
4. Each file that is the tests and calculator can be run by opening the project in pycharm and running them individually.

## Step 3: Creating calculator.py in src Folder
- In this step, we create a Python script named calculator.py within the src folder of your project. This script contains a set of mathematical functions designed to perform basic arithmetic operations.
- add(x, y) adds two input numbers, x and y.
- substract(x, y) subtracts y from x.
- multiply(x, y) multiplies x and y.
- divide(x, y) combines the results of the above functions and returns their sum.
- power(x, y) exponents x with y.

**Using Pytest** <br>
- Installation (if not already installed):
- If you haven't already installed pytest, you can do so using pip:
    ```
    pip install pytest
    ```
    ```
- Pytest automatically discovers test functions based on naming conventions. It searches for functions starting with test_ or ending with _test, and it can discover tests in subdirectories as well. This makes it easy to organize your tests.
- Pytest supports parametrized tests, which allow you to run the same test function with multiple sets of inputs and expected outputs. This is particularly useful for testing functions with different input scenarios. Please refer the commented out code in the test_pytest.py file for your reference.
- Let's create a test file named test_pytest.py within the test folder. This file will contain a series of test functions, each aimed at verifying the behavior of specific functions within calculator.py.
- We've prepared four test functions (test_fun1, test_fun2, test_fun3, and test_fun4) to test the functions within calculator.py. Each test function uses the assert statement to validate the expected outcomes. Refer the file under test folder for your [reference](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/test/test_pytest.py).
- By running these pytest tests, you can verify that your calculator functions are working correctly.

## Step 5. Implementing GitHub Actions
- GitHub Actions is a powerful automation and CI/CD (Continuous Integration/Continuous Deployment) platform provided by GitHub. It enables you to automate various workflows and tasks directly within your GitHub repository. GitHub Actions can be used for a wide range of purposes, such as running tests, deploying applications, and automating release processes.

**How GitHub Actions Work:** <br>

- GitHub Actions work based on events, actions, and triggers:
- **Events:** These are specific activities that occur within your GitHub repository, such as code pushes, pull requests, or issue comments. GitHub Actions can respond to these events.
- **Actions:** Actions are individual tasks or steps that you define in a workflow file. These tasks can be anything from building your code to running tests or deploying your application.
- **Triggers:** Triggers are conditions that cause a workflow to run. They can be based on events (e.g., a new pull request) or scheduled to run at specific times.

**The Purpose of GitHub Actions:** <br>

- GitHub Actions serves several purposes:
- **Automation:** It automates repetitive tasks, reducing manual effort and ensuring consistency in your development process.
- **Continuous Integration (CI):** It allows you to set up CI pipelines to automatically build, test, and validate your code changes whenever new code is pushed to the repository.
- **Continuous Deployment (CD):** It enables automatic deployment of your application when changes are merged into a specific branch, ensuring a smooth and reliable release process.

### Using Pytest and Unittest with GitHub Actions:
- Integrating Pytest and Unittest with GitHub Actions can significantly improve the quality and reliability of your codebase. Here's how:
- Pytest with GitHub Actions: You can create a GitHub Actions workflow (e.g., pytest_action.yml) that specifies the steps for running your Pytest tests. When events like code pushes or pull requests occur, GitHub Actions will automatically trigger the workflow, running your Pytest tests and reporting the results back to you. This helps you catch bugs and ensure that your code meets quality standards early in the development process.
- Unittest with GitHub Actions: Similarly, you can create a separate GitHub Actions workflow (e.g., unittest_action.yml) to run your Unittest tests. This ensures that both your Pytest and Unittest suites are executed automatically whenever code changes are made or pull requests are submitted. It provides a robust validation mechanism for your codebase.
- When collaborating in teams, the automated testing process ensures that all test cases pass successfully before allowing the merge of a pull request into the main branch.

### Creating GitHub Actions Workflow Files:
- To implement Pytest and Unittest with GitHub Actions, you'll create two workflow files under the .github/workflows directory in your repository: pytest_action.yml and unittest_action.yml. These workflow files define the specific actions and triggers for running your tests.

**pytest_action.yml** <br>
Please refer [this](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/workflows/pytest_action.yml) file for your reference
1. Workflow Name: The workflow is named "Testing with Pytest."
2. Event Trigger: It specifies the event that triggers the workflow. In this case, it triggers when code is pushed to the main branch.
3. Jobs: The workflow contains a single job named "build," which runs on the ubuntu-latest virtual machine environment.
4. Steps:
- Checkout code: This step checks out the code from the repository using actions/checkout@v2.
- Set up Python: It sets up the Python environment using actions/setup-python@v2 and specifies Python version 3.8.
- Install Dependencies: This step installs the project dependencies by running pip install -r requirements.txt.
- Run Tests and Generate XML Report: The core testing step runs Pytest with the --junitxml flag to generate an XML report named pytest-report.xml. The continue-on-error: false setting ensures that the workflow will be marked as failed if any test fails.
- Upload Test Results: In this step, the generated XML report is uploaded as an artifact using actions/upload-artifact@v2. The name of the artifact is "test-results," and the path to the report is specified as pytest-report.xml.
- Notify on Success and Failure: These two steps use conditional logic to notify based on the outcome of the tests.
- if: success() checks if the tests passed successfully and runs the "Tests passed successfully" message.
- if: failure() checks if the tests failed and runs the "Tests failed" message.

**unittest_action.yml** <br>
 Please refer [this](https://github.com/raminmohammadi/MLOps/blob/main/Github_Labs/Lab1/workflows/unittest_action.yml) file for your reference
1. Workflow Name: This GitHub Actions workflow is named "Python Unittests."
2. Event Trigger: The workflow is triggered by the "push" event, specifically when changes are pushed to the main branch.
3. Jobs: The workflow defines a single job named "build" that runs on the ubuntu-latest virtual machine environment.
4. Steps:
- Checkout code: This step uses the actions/checkout@v2 action to check out the code from the repository. It ensures that the workflow has access to the latest code.
- Set up Python: The "Set up Python" step uses the actions/setup-python@v2 action to configure the Python environment. It specifies that Python version 3.8 should be used.
- Install Dependencies: This step runs the command pip install -r requirements.txt to install the project's Python dependencies. It assumes that the project's dependencies are listed in the requirements.txt file.
- Run unittests: In this step, the unittest tests are executed using the command python -m unittest test.test_unittest. It runs the unittest test suite defined in the test.test_unittest module.
- Notify on success: This step uses conditional logic with if: success() to check if all the unittest tests passed successfully. If they did, it runs the message "Unit tests passed successfully."
- Notify on failure: Similarly, this step uses conditional logic with if: failure() to check if any of the unittest tests failed. If any test failed, it runs the message "Unit tests failed."
