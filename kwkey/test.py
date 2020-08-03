import doctest

# Modules to be tested.
import kwkey
import kwkey.example_jfine
import kwkey.jfine
import kwkey.sdaprano
import kwkey.test
import kwkey.test_jfine
import kwkey.test_sdaprano
import kwkey.test_K
import kwkey.tools




if __name__ == '__main__':

    # Test the modules.
    for module in (
            kwkey,
            kwkey.example_jfine,
            kwkey.jfine,
            kwkey.sdaprano,
            kwkey.test,
            kwkey.test_jfine,
            kwkey.test_K,
            kwkey.test_sdaprano,
            kwkey.tools,
    ):
        # Run test and print results.
        print(module.__name__, doctest.testmod(module))
