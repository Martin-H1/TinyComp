# Common set of macros to enable Linux versus Windows portability.
ifeq ($(OS),Windows_NT)
    PYTHON = python
    RM = del /f /q
    RMDIR = rmdir /s /q
    SHELL_EXT = bat
    TOUCH = type nul >
else
    PYTHON = python
    RM = rm -f
    RMDIR = rm -rf
    SHELL_EXT = sh
    TOUCH = touch
endif

TESTS = testTokenizer testSchemeParser

.PHONY : tests
tests: $(TESTS)

.PHONY : testTokenizer
testTokenizer:
	$(PYTHON) testTokenizer.py

.PHONY : testSchemeParser
testSchemeParser:
	$(PYTHON) testSchemeParser.py

.PHONY : clean
clean:
	-$(RMDIR) __pycache__
	-$(RM) *.asm
