from production import forward_chain
from rules import TOURIST_RULES, QUESTION_MAP

TOURIST_TYPES = {'American', 'British',
                 'French', 'German', 'Canadian', 'Loonie'}


def expert_system():
    data = []
    rejected_tourists = []
    while True:
        for fact, question in QUESTION_MAP.items():
            if fact not in data:
                answer = input(f"{question} (yes/no): ").strip().lower()
                if answer == 'yes':
                    data.append(f'tourist {fact}')
                else:
                    data.append(f'not tourist {fact}')

            inferred_facts = forward_chain(TOURIST_RULES, data)

            for fact in inferred_facts:
                if any(tourist in fact for tourist in TOURIST_TYPES) and fact.split()[-1] not in rejected_tourists:
                    tourist_type = fact.split()[-1]
                    confirm = input(f"Is the tourist {
                                    tourist_type}? (yes/no): ").strip().lower()
                    if confirm == 'yes':
                        print(f"The tourist is {tourist_type}.")
                        return
                    else:
                        print("Let's continue asking questions.")
                        print("\n")
                        rejected_tourists.append(tourist_type)
                    break

        print("Couldn't deduce the tourist type yet, asking more questions...")


if __name__ == '__main__':
    expert_system()
