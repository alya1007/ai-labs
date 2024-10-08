from production import IF, AND, THEN, FAIL, OR

TOURIST_RULES = (
    IF(OR('(?x) has messy hair', '(?x) has a long beard'),
        THEN('(?x) does not care about style')),

    IF(AND('(?x) does not care about style', '(?x) wears a red plaid shirt', '(?x) apologizes a lot'),
        THEN('(?x) is Canadian')),

    IF(OR('(?x) apologizes a lot', '(?x) is friendly'),
        THEN('(?x) is polite')),

    IF(OR('(?x) has a flag on T-Shirt', '(?x) says "God save the king" a lot'),
        THEN('(?x) is patriotic')),

    IF(AND('(?x) is patriotic', '(?x) visits fast food places', '(?x) smiles a lot'),
        THEN('(?x) is American')),

    IF(OR('(?x) is loud', '(?x) visits local pubs'),
        THEN('(?x) drinks a lot')),

    IF(AND('(?x) is patriotic', '(?x) has a weird accent', '(?x) drinks a lot', '(?x) is polite'),
        THEN('(?x) is British')),

    IF(AND('(?x) does not curse', '(?x) is polite'),
        THEN('(?x) respects rules')),

    IF(AND('(?x) drinks a lot', '(?x) has blonde hair and blue eyes', '(?x) respects rules', '(?x) is always on time'),
        THEN('(?x) is German')),

    IF(OR('(?x) visits museums', '(?x) visits traditional restaurants'),
        THEN('(?x) is interested in culture')),

    IF(AND('(?x) is interested in culture', '(?x) is stylish'),
        THEN('(?x) is intellectual')),

    IF(AND('(?x) is intellectual', '(?x) wears a scarf'),
        THEN('(?x) is French')),

    IF(AND('(?x) is interested in culture', '(?x) speaks local language'),
        THEN('(?x) is Loonie')),
)

QUESTION_MAP = {
    'has messy hair': "Does the tourist have messy hair?",
    'has a long beard': "Does the tourist have a long beard?",
    'wears a red plaid shirt': "Is the tourist wearing a red plaid shirt?",
    'apologizes a lot': "Does the tourist apologize a lot?",
    'is friendly': "Is the tourist friendly?",
    'has a flag on T-Shirt': "Does the tourist have a flag on their T-Shirt?",
    'says "God save the king" a lot': "Does the tourist say 'God save the king' a lot?",
    'smiles a lot': "Does the tourist smile a lot?",
    'is loud': "Is the tourist loud?",
    'has a weird accent': "Does the tourist have a weird accent?",
    'does not curse': "Does the tourist not curse?",
    'has blonde hair and blue eyes': "Does the tourist have blonde hair and blue eyes?",
    'is always on time': "Is the tourist always on time?",
    'visits museums': "Does the tourist visit museums?",
    'is stylish': "Is the tourist stylish?",
    'wears a scarf': "Is the tourist wearing a scarf?",
    'speaks local language': "Does the tourist speak the local language?",
}
