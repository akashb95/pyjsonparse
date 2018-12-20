# JSON Lexer/Parser
_Author: Akash Bhattacharya_

## Overview
This is a submission for the COMP0069 Compilers coursework. This aim of this project was to build a JSON lexer/parser using Python-Lex-Yacc (PLY) that will read a stream of characters, and decide whether or not it is in valid JSON format. 

## Prerequisites
This project has been tested and confirmed working on Python3.7 and PLY version 3.11. 

## Usage
The main magic happens in the `JSON_lex.py` with `JSON_parse.py`, so needless to say, these should be left untouched.

To run a one-off test, you can create a `.py` file and import the parser from the JSON_parse file:

```from JSON_parse import JSONParser```

After this, you will need to create an instance of this parser:

```p = JSONParser()```

Finally, give it some text input as a **raw string** to see it work:

```
text = r"""{"Sample": "Object", "List": [1, 2, 3], "Another": "\u0001 Value"}""" 
p.parse(text)
```

This should exit with status 0, which means that the JSON is valid. If any input raises a SyntaxError, then there's a syntax error in the JSON (assuming it's not your Python snippets).

## Testing
There's also a `tests.py` file that runs the parser on a series of JSON files in the `./tests/` directory. Simply add some more JSON files in the same naming format to the pre-existing ones if you want to do some batch-testing. You'll also need to change the `NUM_TESTING_FILES` parameter near the top of `tests.py`. The results are outputted into `./tests/test_results.log`.

## Structure
The definition of all the valid tokens in a JSON format are specified in the `JSONLexer` class in `JSON_lex.py`. Although this could have been done without defining a separate class for the Lexer, I chose to do so because it facilitates the monitoring of states. For example, I have implemented a simple feature to detect whether an object or an array has been open/closed properly. If required, such a structure makes it easy to implement more advanced features that require statefulness.

The `JSONLexer` class contains all the required Regular Expressions (RegEx) for correctly tokenising a sample JSON input as class attributes as per the JSON spec. Some of the tokens' regexes are defined as class attributes, but the token definitions themselves are represented as class methods. This is because I've implemented some additional functionality to perform some tasks when this regex expression is matched. As per the PLY spec, all token definitions begin with the substring `t_`.

To make debugging easier, every time a newline character is found, the `lexer.lineno` variable is incremented. Also, when a left brace or bracket is detected, the 'depth' of the corresponding data structure is stored in the `JSONLexer` class so as to detect unclosed braces/brackets. If an unexpected token is detected, an error is raised, and parsing subsequently stops, because we know the JSON is invalid. The `build` method is actually responsible for building the lexer. The `test` method is to make testing the lexer easier. Note this does no syntax checks, but simply tokenises the input stream according to the rules defined in the class. Finally, the `input` and `token` methods are to ensure yacc.yacc() works with our custom lexer class, and passes some variables to it when required.

The `JSONLexer` class is called from the corresponding `JSONParser` class in `JSON_parse.py`. The role of this class is to make sure that the tokens that we get from the lexer is correctly "arranged", i.e. has the correct syntax and grammar. Such rules (i.e. grammar specifications) are all defined as methods of the class. As per the PLY spec, all such definitions begin with the substring `p_`.

In the `JSONParser.__init__()` function, a lexer instance is called, and the lexer is built. The defined tokens are also loaded in as instance variables. Finally, the `yacc.yacc()` function (the compiler) is called. The 'start' keyword ensures that the parsing must begin semantics defined in `p_start`, which could be either an array or an object (as the JSON spec dictates). The definition of an 'object', an 'array', and other structures are represented as class methods.

An 'object' must begin with an LBRACE token, and end with the RBRACE token, and in between, there can be 0 or more 'pairs', each of which should be a STRING: 'value' pair, and so on. All this is methodically described in very recursive patterns in the `JSONParser` methods. The `JSONParser.p_error()` method raises a Syntax Error when one is detected, stopping the parsing as the JSON is invalid. Finally, the `JSONParser.parse(text)` method makes the parsing start, taking a raw string as the input candidate JSON object.

There is also a directory, `tests` which contains several JSON files, some of which are valid and some which are invalid. A `tests.py` script runs batch tests to check the validity of these files, and outputs the `stdout` and `stderr` to `test_results.log`.