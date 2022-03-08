import fitz
import re
 
class Redactor:
    @staticmethod
    def get_sensitive_data(lines):                
        """ EMAIL REGEX """
        EMAIL_REG = r"([\w\.\d]+\@[\w\d]+\.[\w\d]+)"

        for line in lines:
            """ Empty Line """
            if len(str(line).strip()) == 0:
                continue
            
            """ MATCH EMAIL """
            if re.search(EMAIL_REG, line, re.IGNORECASE):
                search = re.search(EMAIL_REG, line, re.IGNORECASE)
                
                """
                    Yields creates a generator
                    Generator is used to return values in between function iterations
                """
                yield search.group(1)
 
    # constructor
    def __init__(self, filename):
        self.filename = filename
 
    def redaction(self):         
        """ Open PDF """
        doc = fitz.open(self.filename)
        
        """ Iterate through PDF pages """
        for page in doc:
            """ Get Page Text """
            page.get_text()

            """ Get Sensitive Data to Replace """
            sensitive = self.get_sensitive_data(page.get_text("text").split('\n'))

            """ Iterate Sensitive Data """
            for data in sensitive:
                areas = page.search_for(data)
                 
                """ Change Sensitive Data """
                star = ["*" for i in range(len(data))]
                [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]
                # [page.add_redact_annot(area, text = str("").join(star)) for area in areas]
                 
            # Apply Reduction
            page.apply_redactions()
             
        """ Save New Data """
        reductionFileName = str(str(self.filename).split(".")[0] + '-redaction.pdf').lower()
        doc.save(reductionFileName)
        print("")
        print("")
        print("==========================================")
        print(reductionFileName + " successfully redacted.")
        print("==========================================")
 
# driver code for testing
if __name__ == "__main__":
   
    """ Redaction File Name """
    filename = "resume.pdf"
    redactor = Redactor(filename)
    redactor.redaction()