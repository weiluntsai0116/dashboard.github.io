import subprocess as cmd


def process(fn):

    # try:
    #     cp = cmd.run(f"pytest -s ./tests/test_dash.py --app {fn}", check=True, shell=True)
    #     print(cp)
    # except:
    #     print("Input dash file can't be compiled successfully.")
    #     exit(2)
    #     # return False

    try:
        cp = cmd.run("git add .", check=True, shell=True)
        print("Git add: ")
        print(cp)
        message = "update"
        cp = cmd.run(f"git commit -m '{message}'", check=True, shell=True)
        print("Git commit: ")
        print(cp)

        cp = cmd.run("git push -u origin main -f", check=True, shell=True)
        print("Git push: ")
        print(cp)

    except:
        print("Didn't upload to github. ")
        exit(2)
        # return False


if __name__ == "__main__":
    process("user0_signal3")
