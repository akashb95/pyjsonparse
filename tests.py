from JSON_parse import JSONParser
import sys
import os


def run(num_tests):
    """
    Rather limited function that runs the parser on JSON test files that must be specifically numbered.
    The function iterates through test1.json, test2.json... test<num_test>.json. If an expected file is missing,
    then it skips to the next filename.
    :param num_tests: test file number to iterate up to.
    :return:
    """
    # make parser instance
    parser = JSONParser()

    # input log file path
    log_fname = "test_results.log"
    log_path = os.path.join(os.getcwd(), "tests", log_fname)

    # create log file
    with open(log_path, "w") as f:
        f.write("******** Running Tests *********** \n\n\n")

    # put all stdout and stderr into logfile
    sys.stdout = open(log_path, "a")
    sys.stderr = open(log_path, "a")

    for num in range(num_tests):
        try:
            # get test json file path
            test_fname = "test" + str(num + 1) + ".json"
            test_path = os.path.join(os.getcwd(), "tests", test_fname)

            # read json to memory
            with open(test_path, "r") as f:
                inp = f.read()

            # put json in logfile
            with open(log_path, "a") as f:
                f.write("------{name} INPUT------\n".format(name=test_fname))
                f.write(inp)
                f.write("\n\n\n-------RESULTS------\n")

            # parse the input and output to logfile whether valid or invalid, plus any errors raised.
            try:
                r = parser.parse(text=inp)

                if r:
                    with open(log_path, "a") as f:
                        f.write("Valid JSON.\n\n")

            except SyntaxError as e:
                with open(log_path, "a") as f:
                    f.write(str(e) + "\n")
                    f.write("Invalid JSON.\n\n\n")

        except FileNotFoundError:
            pass
    return


if __name__ == "__main__":
    run(16)
