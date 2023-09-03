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
        # os.mkdir("{}/Disposal Forms {}/DRF Forms".format(path, timestamp))
        # os.mkdir("{}/Disposal Forms {}/TLU Forms".format(path, timestamp))
        # os.mkdir("{}/Disposal Forms {}/PAS Letters".format(path, timestamp))
        return "{}/Disposal Forms {}".format(path, timestamp)
    except SystemError:
        print("ERROR: Failed to create disposal forms directory")


def generateDRF(fields, path):
    try:
        drf.render(fields)
        drf.save("{}/{}/{} DRF.docx".format(path, fields.get('transfer'), fields.get('transfer')))
    except RuntimeError:
        print("ERROR: Transfer {} - Failed to generate DRF form".format(fields.get('transfer')))


def generateTLU(fields, path):
    try:
        tlu.render(fields)
        tlu.save("{}/{}/{} TLU.docx".format(path, fields.get('transfer'), fields.get('transfer')))
    except RuntimeError:
        print("ERROR: Transfer {} - Failed to generate TLU form".format(fields.get('transfer')))


def generateLetter(fields, path):
    try:
        letter.render(fields)
        letter.save("{}/{}/{} PAS Records Disposal Letter.docx".format(path, fields.get('transfer'), fields.get('transfer')))
    except RuntimeError:
        print("ERROR: Transfer {} - Failed to generate PAS letter".format(fields.get('transfer')))


def generateAll(fields_list, path, flag_df):
    forms_path = createDirectories(path)
    print("Disposal form directory created at {}".format(forms_path))

    if len(flag_df) != 0:
        warning_log = open("{}/warning_log.txt".format(forms_path), "w+")
        warning_log.write("DATA WARNING:\n\nThe {} boxes in the table below have been marked to be disposed, but inconsistent/contradictory data has been cross referenced from the master spreadsheet based on the values from the following columns:\n\n'Disposal' > {}:\t\t\t\t\t\t\tBox has not met retention period\n'Status' = 'Shredded':\t\t\t\t\t\t\tBox has already been disposed\n'Status' = 'TLU - Review':\t\t\t\t\t\tBox has been previously submitted for disposal and is under review by TLU\n'Status' = 'PAS - Review' OR 'PAS - Appraisal':\t\t\t\tBox has been previously submitted for disposal and is under review by PAS\n'Status' = 'PAS - Approval':\t\t\t\t\t\tBox has been previously submitted for disposal and is already approved by PAS\n'Branch / Board / Program' AND 'Disposal' AND 'Status' = 'nan':\t\tBox is not present master spreadsheet\n\n{}\n\nEach of the transfer directories containing boxes from the list above are flagged with '-w'".format(len(flag_df), datetime.datetime.now().strftime("%Y"), flag_df.to_string(index=False)))
        warning_log.close()
        print("WARNING: Data inconsistencies and/or contradictions found between master spreadsheet and disposal list for {} boxes. See 'warning_log.txt' in disposal forms directory for details.".format(len(flag_df)))

    print("File generation in progress...")
    for fields in fields_list:
        os.mkdir("{}/{}".format(forms_path, fields.get('transfer')))
        generateDRF(fields, forms_path)
        generateTLU(fields, forms_path)
        generateLetter(fields, forms_path)

    print("File generation complete.")