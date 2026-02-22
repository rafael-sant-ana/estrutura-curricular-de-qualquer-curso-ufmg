from src.classes.PdfProcessor import PdfProcessor

def main():
  fname = "grade-farmacia.pdf"

  pdf = PdfProcessor(fname)
  subjects = pdf.get_subjects_by_semester()
  
  for i in range(len(subjects)): 
    print(f'semestre {i+1}')
    print([str(subject) for subject in subjects[i]])
    print()

if __name__ == "__main__":
  main()
