import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
from io import StringIO

file = st.file_uploader('sen2 xml')

def get_values(xml_elements, table_dict: dict, xml_block):
    for element in xml_elements:
        try:
            table_dict[element] = xml_block.find(element).text
        except:
            table_dict[element] = pd.NA
    return table_dict 

class XMLtoCSV():
    header = pd.DataFrame(
        columns = [
            'Collection',
            'Year',
            'Reference Date'
        ]
    )

    persons = pd.DataFrame(
        columns = [
            'Surname',
            'Forename',
            'PersonBirthDate',
            'Sex',
            'Ethnicity',
            'PostCode',
            'UPNunknown',
        ]
    )

    requests = pd.DataFrame(
        columns = [
            
        ]
    )

    def __init__(self, root):
        header = root.find('Header')
        self.Header = self.create_header(header)

 

    def create_header(self, header):

        header_dict = {}
        collection_details = header.find('CollectionDetails')
        collection_elements = ['Collection', 'Year', 'ReferenceDate'] 
        header_dict = get_values(collection_elements, header_dict, collection_details)

        source = header.find("Source")
        source_elements = [
            "SourceLevel",
            "LEA",
            "SoftwareCode",
            "Release",
            "SerialNo",
            "DateTime",
        ]
        header_dict = get_values(source_elements, header_dict, source)

        header_df = pd.DataFrame.from_dict([header_dict])
        return header_df    


def convert_data(root: ET.Element):
    datafiles = XMLtoCSV(root)

    return datafiles

if file:
    root = ET.fromstring(file.read().decode("utf-8"))
    st.write(root)

    data_files = convert_data(root)

    st.write(data_files.Header)