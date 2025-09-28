import streamlit as st
import pandas as pd
from io import BytesIO

def main():
    database = get_file()

    if "step" not in st.session_state:
        st.session_state.step = 0

    if st.session_state.step == 0:
        if st.button("Dalej") and database:
            st.session_state.database = load_database(database)
            st.session_state.mappings = display_uniques(st.session_state.database)
            st.session_state.step = 1

    elif st.session_state.step == 1:
        st.session_state.mappings = display_uniques(st.session_state.database, st.session_state.mappings)

        if st.button("Enkoduj"):
            df_encoded = apply_encoding(st.session_state.database.copy(), st.session_state.mappings)

            towrite = BytesIO()
            with pd.ExcelWriter(towrite, engine='openpyxl') as writer:
                st.session_state.database.to_excel(writer, index=False, sheet_name="Baza rozkodowana")
                df_encoded.to_excel(writer, index=False, sheet_name="Baza zakodowana")
                mappings_concat = pd.concat(
                            {col: df for col, df in st.session_state.mappings.items()},
                            names=["Pytanie"]
                            ).reset_index(level=0).rename(columns={"level_0": "Pytanie"})
                mappings_concat.to_excel(writer, index=False, sheet_name="Księga kodów")

            towrite.seek(0)

            st.download_button(
                label="Pobierz jako Excel",
                data=towrite,
                file_name="encoded_database.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )


def display_uniques(df, mappings=None):
    if mappings is None:
        mappings = {}

    for column in df.columns:
        uniques = df.loc[df[column] != 999, column].dropna().unique()

        if df[column].dtype in ["float64", "int64"]:
            continue

        if set(["Tak", "Nie wybrano"]).issubset(set(uniques)):
            mappings[column] = pd.DataFrame({
                "Wartość": ["Tak", "Nie wybrano"],
                "Kod": [1, 0]
            })
            mappings[column] = st.data_editor(
                mappings[column],
                num_rows="dynamic",
                key=f"editor_{column}"
            )
            continue

        if column not in mappings:
            mappings[column] = pd.DataFrame({
                "Wartość": uniques,
                "Kod": range(1, len(uniques) + 1)
            })
        st.write(f"### {column}")
        mappings[column] = st.data_editor(
            mappings[column],
            num_rows="dynamic",
            key=f"editor_{column}"
        )
    return mappings


def apply_encoding(df, mappings):
    for column, mapping_df in mappings.items():
        map_dict = dict(zip(mapping_df["Wartość"], mapping_df["Kod"]))
        df[column] = df[column].map(map_dict)

    df = df.fillna(999)
    return df


def load_database(database):
    if database.name.endswith(".csv"):
        return pd.read_csv(database)
    else:
        return pd.read_excel(database)


def get_file():
    return st.file_uploader('Plik excel/csv', ['csv', 'xlsx'])


main()