from string import ascii_lowercase
import pandas as pd

questions = {
    "'Are you a neutral or stability runner?'" : ["Neutral", "Stability"],
    "'Do you have any of the following injuries?'" : ['Achilles Tendonitis', 'Plantar Fascitis', 'Bunions', 'Knee Pain', 'None'],
    "'How much cushion do you like?'" : ['Low', 'Medium', 'High'],
    "'Is weight a big factor for you?'" : ['Yes', 'No'],
    "'Where does your foot strike when you run?'" : ['Forefoot', 'Midfoot', 'Heel Strike'],
    "'What is your price range?'" : ['Under 100', '100-150', '150-200', '200+']
}

user_answer = []
for num, (question, alternatives) in enumerate(questions.items(), start = 1):
    print(f"\nQuestion {num}:")
    print(f"{question}")
    labeled_alternatives = dict(zip(ascii_lowercase, sorted(alternatives)))
    for label, alternative in labeled_alternatives.items():
        print(f" {label}) {alternative}")
    
    answer_label = input("\nChoice(in letter)? ")
    user_answer.append(labeled_alternatives.get(answer_label))

if user_answer[0] == 'Neutral':
    run_df = pd.read_csv('C:/Users/natal/OneDrive/Documents/natalie-code/csv/shoe_neutral.csv')
    df = run_df.copy()
elif user_answer[0] == 'Stability' or user_answer[2] == 'Knee Pain':
    run_df = pd.read_csv('C:/Users/natal/OneDrive/Documents/natalie-code/csv/shoe_stability.csv')
    df = run_df.copy()

if user_answer[1] == 'Achilles Tendonitis':
    df = df[df['drop'] >= 8]
if user_answer[1] == 'Plantar Fascitis' or user_answer[2] == 'Bunions' or user_answer[2] == 'High':
    df = df[df['category'].isin(['Neutral Cushion - High'])]

if user_answer[2] == 'Low':
    df = df[df['category'].isin(['Neutral Cushion - Light'])]
if user_answer[2] == 'Medium':
    df = df[df['category'].isin(['Neutral Cushion - Medium'])]

if user_answer[3] == 'Yes':
    df = df[df['weight'] <= 250]

if user_answer[4] == 'Forefoot':
    df = df[df['drop'] <= 4]
elif user_answer[4] == 'Midfoot':
    df = df[df['drop'] >=5]
    df = df[df['drop']<10]
elif user_answer[4] == 'Heel Strike':
    df = df[df['drop']>=10]

if user_answer[5] == 'Under 100':
    df = df[df['price']<100]
elif user_answer[5] == '100-150':
    df = df[df['price']>=100]
    df = df[df['price']<150]
elif user_answer[5] == '150-200':
    df = df[df['price']>=150]
    df = df[df['price']<200]
elif user_answer[5] == '200+':
    df = df[df['price']>200]


print(user_answer)
print(df)