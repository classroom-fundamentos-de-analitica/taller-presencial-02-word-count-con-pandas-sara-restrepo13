"""Taller evaluable"""

import glob

import pandas as pd


def load_input(input_directory):
    """Load text files in 'input_directory/'"""
    #
    # Lea los archivos de texto en la carpeta input/ y almacene el contenido en
    # un DataFrame de Pandas. Cada línea del archivo de texto debe ser una
    # entrada en el DataFrame.
    #

    filenames=glob.glob(input_directory+'/*.*')
    dataframes=[pd.read_csv(filename,sep=";",names=['text']) for filename in filenames] #No tengo columna con nombre de las filas
    dataframe=pd.concat(dataframes).reset_index(drop=True)  #Varios concat en una lista y los pega todos uno debajo del otro
    return dataframe


def clean_text(dataframe):
    """Text cleaning"""
    #
    # Elimine la puntuación y convierta el texto a minúsculas. - Primero hacer copia para poder modificar con tranquilidad
    #
    dataframe=dataframe.copy()
    dataframe['text']=dataframe['text'].str.lower()
    dataframe['text']=dataframe['text'].str.replace(",","").str.replace(".","")
    return dataframe


def count_words(dataframe):
    """Word count"""
    dataframe=dataframe.copy()
    dataframe['text']=dataframe['text'].str.split() #Crear una lista de palabras
    dataframe=dataframe.explode('text').reset_index(drop=True) #Trasponer, del ancho al largo
    dataframe=dataframe.rename(columns={'text':'word'})
    dataframe['count']=1

    conteo=dataframe.groupby(['word'], as_index=False).agg({'count':sum}) #Fn generica de pandas que me dice como agrego las columnas
    return conteo


def save_output(dataframe, output_filename):
    """Save output to a file."""
    dataframe.to_csv(output_filename, index=False, sep="\t")


#
# Escriba la función job, la cual orquesta las funciones anteriores.
#
def run(input_directory, output_filename):
    """Call all functions."""

    dataframe=load_input(input_directory)
    dataframe=clean_text(dataframe)
    dataframe=count_words(dataframe)
    save_output(dataframe,output_filename)

    


if __name__ == "__main__":
    run(
        "input",
        "output.txt",
    )
