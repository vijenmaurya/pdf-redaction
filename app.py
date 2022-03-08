import fitz
import re
 
class Redactor:
    @staticmethod
    def get_sensitive_data(lines):        
        """ EXACT MATCH REGEX """
        SEARCH_STRINGS = [
            "Subharti University, Meerut — BCA",
            "Vijendra"
        ]
        EXACT_MATCH = r'^(' + "|".join(SEARCH_STRINGS) + ')'

        for line in lines:
            """ Empty Line """
            if len(str(line).strip()) == 0:
                continue
            
            """ Find String """
            for string in SEARCH_STRINGS:
                if str(string).lower() in str(line).lower():
                    print("Search: ", string, "Line: ", line)
                    yield string
 
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
                print("Area", areas)
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
    file = "resume"
    extension = ".pdf"
    filename = file + extension
    redactor = Redactor(filename)
    redactor.redaction()