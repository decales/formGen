import os
import datetime
from docxtpl import DocxTemplate

drf = DocxTemplate('templates/DRF.docx')
tlu = DocxTemplate('templates/TLU.docx')
letter = DocxTemplate('templates/PAS Records Disposal Letter.docx')

def createDirectories(path):
    try:
        timestamp = datetime.datetime.now().strftime('%H%M%S')
        os.mkdir("{}/Disposal Forms {}".format(path, timestamp))
        os.mkdir("{}/Disposal Forms {}/DRF Forms".format(path, timestamp))
        os.mkdir("{}/Disposal Forms {}/TLU Forms".format(path, timestamp))
        os.mkdir("{}/Disposal Forms {}/PAS Letters".format(path, timestamp))
        return "{}/Disposal Forms {}".format(path, timestamp)
    except:
        print("Failed to create disposal forms directory")


def generateDRF(fields, path):
    try:
        drf.render(fields)
        drf.save("{}/DRF Forms/{} DRF.docx".format(path, fields.get('transfer')))
    except Exception:
        print("Failed to generate DRF form {}".format(fields.get('transfer')))


def generateTLU(fields, path):
    try:
        tlu.render(fields)
        tlu.save("{}/TLU Forms/{} TLU.docx".format(path, fields.get('transfer')))
    except Exception:
        print("Failed to generate TLU form {}".format(fields.get('transfer')))


def generateLetter(fields, path):
    try:
        letter.render(fields)
        letter.save("{}/PAS Letters/{} PAS Records Disposal Letter.docx".format(path, fields.get('transfer')))
    except Exception:
        print("Failed to generate letter {}".format(fields.get('transfer')))


def generateAll(fields_list, path):
    forms_path = createDirectories(path)
    print("Disposal form directory created at {}\nBeginning file generation...".format(forms_path))
    for fields in fields_list:
        generateDRF(fields, forms_path)
        generateTLU(fields, forms_path)
        generateLetter(fields, forms_path)
    print("File generation complete.")