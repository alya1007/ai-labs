from rules import TOURIST_RULES
from production import backward_chain


def main():
    statement = 'Tourist is ' + input("Complete the sentence: Tourist is ")
    backward_chain_goal_tree = backward_chain(TOURIST_RULES, statement)

    print("Goal tree structure:", backward_chain_goal_tree)


if __name__ == "__main__":
    main()
