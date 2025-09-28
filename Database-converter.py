import pandas as pd
import numpy as np
import os

###TODO: 
#Tworzenie zakładki księga kodów
#Drag-and-drop window
###

def main():

    tags = ['[w]', '[W]', '[o]', '[O]']

    try:

        # Import bazy
        df = pd.read_excel("C:/Users/"+os.environ.get('USERNAME')+"/Desktop/Test.xlsx")

        try:
            #TODO: restrukturyzacja, dwie bazy chyba nie są potrzebne

            dfnew = pd.DataFrame(df)
            dfexport = pd.DataFrame(df)
            keys_table = pd.DataFrame(columns=3)

            for col in dfnew.columns:

                #Zdefiniowanie wartości unikatowych w kolumnie, usunięcie 999 z listy unikatów
                unique_values = df[col].unique() 
                true_unique_values = is_missing_value(unique_values)

                #Sprawdzenie, czy kolumna zawiera wartości liczbowe, jeżeli tak to ją zostawiamy bez zmian
                if dfnew[col].values.all == is_numeric(dfnew[col].values):
                    continue
                else:
                    #Zakodowanie zmiennych jakościowych, sprawdzanie, czy pytanie jest wielokrotnego wyboru
                    if is_tags_multiple_choice_question(col, tags) == True:
                        compare = {value: id for id, value in enumerate(true_unique_values)}
                    else:
                        compare = {value: id + 1 for id, value in enumerate(true_unique_values)}

                for id in compare:
                    print(id)
                
                #Sprawdzenie, czy kolumna zawiera odpowiedzi z pytania otwartego, jeżeli tak, zostawiamy ją bez zmian
                if is_tags_open_question(col, tags):
                    dfexport[col] = df[col]
                else:
                    dfexport[col] = df[col].map(compare).fillna(df[col])


            with pd.ExcelWriter("C:/Users/"+os.environ.get('USERNAME')+"/Desktop/Output.xlsx", mode='w') as writer:
                df.to_excel(writer, sheet_name='Baza zakodowana')
                dfexport.to_excel(writer, sheet_name='Baza rozkodowana')

        except:
            raise TypeError('Error:')
    except FileNotFoundError:
        raise TypeError('Error:', FileNotFoundError)


#Sprawdzenie, czy w kolumnie jest wartość '999', jeżeli tak, to ją wyrzucamy z listy unikatowych kategorii
def is_missing_value(unique):
    true_unique_values = np.array([])
    if 999 in unique:
        for i in unique:
            if i != 999:
                true_unique_values = np.append(true_unique_values, i)
    else:
        true_unique_values = unique
    return true_unique_values

#Sprawdzenie, czy w kolumnie są tylko wartości ilościowe
def is_numeric(x):
    if isinstance(x, (int,float, complex)):
        return True
    else:
        return False
    
#Sprawdzenie, tag w nazwie kolumny oznacza pytanie otwarte
def is_tags_open_question(col, tags):
    passer = False
    for x in tags[2:4]:
        if x in col:
            if passer:
                continue
            else:
                passer = True
    return passer

#Sprawdzenie, tag w nazwie kolumny oznacza pytanie wielokrotnego wyboru
def is_tags_multiple_choice_question(col, tags):
    passer = False
    for x in tags[:2]:
        if x in col:
            if passer:
                continue
            else:
                passer = True
    return passer

main()