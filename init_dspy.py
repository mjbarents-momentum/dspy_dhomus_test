import dspy
from pdf2table import pdf_to_base64_image, get_csv_tabel

class GenerateQuestion(dspy.Signature):
    """Generate a question that must be validated, based on the 'omschrijving' column of the first row."""

    df = dspy.InputField(desc="Table with 'omschrijving' column")
    question = dspy.OutputField(desc="A question that must be validated")

class ValidateQuestion(dspy.Signature):
    """Validate if the question can be answered"""

    question = dspy.InputField()
    answer = dspy.OutputField(desc="Yes or no")

class Questioner(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_questions = dspy.ChainOfThought(GenerateQuestion)

    def forward(self, df):
        question = self.generate_questions(df=df)
        return question
    
class Validator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.validate_question = dspy.ChainOfThought(ValidateQuestion)

    def forward(self, question):
        answer = self.validate_question(question=question)  
        return answer

def init_dspy(pdf_file_path, pdf_file_page):
    base64_image = pdf_to_base64_image(pdf_file_path, first_page=pdf_file_page, last_page=pdf_file_page)
    df = get_csv_tabel(base64_image)

    # Generate a question based on the base64_image
    question_agent = Questioner()
    pred = question_agent(df)

    # Validate the generated question
    validate_agent = Validator()
    val = validate_agent(pred.question)

    # Print the question and validation
    print('Question: ', pred.question)
    print('Can it be validated?: ', val.answer, '\n')

if __name__ == "__main__":
    pdf_file_path = input("Enter the path to the PDF file: ")
    pdf_file_page = input("Enter the page number: ")

    # Set up the LM
    print("\n Initalizing DSPy ... \n")
    gpt_4o = dspy.LM(model='gpt-4o')
    dspy.settings.configure(lm=gpt_4o)
    init_dspy(pdf_file_path, int(pdf_file_page))


  