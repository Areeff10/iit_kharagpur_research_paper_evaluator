from PyPDF2 import PdfReader
import os 
import pandas 

choice = input('0:pub\n1:non-pub\n2:papers : ')
if choice == '1':
    loc = r'Reference\Non-Publishable'
elif choice == '0':
    loc = r'Reference\Publishable'
else:
    loc = 'Papers'

def readPDF(file):
    name = file.split('\\')[-1]
    size = os.path.getsize(file)
    reader = PdfReader(file)
    pages = len(reader.pages)
    sections = 0
    subSections = 0
    completedSections = []
    completedSubSections = []
    text = ''
    for i in range(pages):
        page = reader.pages[i]
        text += page.extract_text() + '\n'
    texts = text.split('\n')
    for line in texts:
        words = line.split(' ')
        try:
            if words[0] not in completedSections and words[0] not in completedSubSections:
                if words[0].isdigit():
                    if words[1].isalnum() and len(words) < 10:
                        completedSections.append(words[0])
                        sections += 1
                elif '.' in words[0]:
                    digits = words[0].split('.')
                    subsectionparts = list(filter(lambda x: x.isdigit() , digits))
                    if digits == subsectionparts and words[1].isalnum() and len(words) < 10:
                        completedSubSections.append(words[0])
                        subSections += 1

        except:
            pass 
    return [name, pages , sections , subSections , size]

data = {
    'name': [],
    'pages': [],
    'sections': [],
    'subSections': [],
    'size': []
}

for file in os.listdir(loc):
    if '.' not in file:
        for file_ in os.listdir(fr"{loc}\{file}"):
            pdfInfo = readPDF(rf'{loc}\{file}\{file_}')
            data['name'].append(pdfInfo[0]) 
            data['pages'].append(pdfInfo[1]) 
            data['sections'].append(pdfInfo[2]) 
            data['subSections'].append(pdfInfo[3]) 
            data['size'].append(pdfInfo[4]) 
         
    else:
        pdfInfo = readPDF(rf'{loc}\{file}')
        data['name'].append(pdfInfo[0]) 
        data['pages'].append(pdfInfo[1]) 
        data['sections'].append(pdfInfo[2]) 
        data['subSections'].append(pdfInfo[3]) 
        data['size'].append(pdfInfo[4]) 
         

df = pandas.DataFrame(data)
df.to_csv(f"{loc.split('\\')[-1]}.csv", index=False)