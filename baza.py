import pandas as pd
import streamlit as st
import altair as alt

try:
 data1 = st.file_uploader("załaduj dane z GISAID", type=["tsv", "txt"]) 				#laduje dane

 dfadd = pd.read_csv(data1, sep = '\t')
 dfread = pd.read_csv('/home/piotr/Desktop/gis24/gisbaza/0809.tsv', sep = '\t')
 
 frames = [dfadd, dfread]
 
 result = pd.concat(frames)
 result = result.drop_duplicates()
 
 result.to_csv('/home/piotr/Desktop/gis24/gisbaza/0809.tsv', sep = '\t')
 
 dbf = pd.read_csv('/home/piotr/Desktop/gis24/gisbaza/0809.tsv', sep = '\t')
 
 df_iz = dbf[['strain', 'date', 'country', 'division','location', 'age', 'sex','pangolin_lineage','GISAID_clade', 'originating_lab', 'submitting_lab', 'date_submitted']] 			#wybiera odpowiednie kolumny
 
 db_iz = pd.DataFrame(df_iz.groupby(['pangolin_lineage', 'date_submitted']).size(), columns = ['count'])			#grupuje wg lini virusa i daty dodania
 db_iz.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 db_iz.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 
 dat_final = db_iz.sort_values(by=['date_submitted'], ascending=True)	 #sortowanie wg daty
 
 dat_final = dat_final[dat_final['count'] >10]
 
 
 #wykres
 selection = alt.selection_multi(fields=['pangolin_lineage'], bind='legend')
 
 
 chart_waw = alt.Chart(dat_final).mark_line(point=True).encode(
    x ='date_submitted', 
    y='count',
    color='pangolin_lineage',
    strokeDash='pangolin_lineage',
    order='date_submitted',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).interactive().properties(
    width=800,
    height=500
 ).add_selection(selection)
 
 st.write('')
 st.write('Warianty w zależności od daty dodania')
 chart_waw
 
 
 db_iz1 = pd.DataFrame(dbf.groupby(['country', 'pangolin_lineage', ]).size(), columns = ['count'])			#grupuje wg lini virusa i kraju
 db_iz1.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 db_iz1.reset_index(level=0, inplace=True)				#resetuje indeksy kolumny
 db_iz1 = db_iz1[db_iz1['count']>10]
 
 chart_c = alt.Chart(db_iz1).mark_bar(
    cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3
    ).encode(
    x='count',
    y='country',
    color='pangolin_lineage',
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
    ).properties( width=800,
    height=500).add_selection(selection)
 
 chart_c

except:
 pass
 