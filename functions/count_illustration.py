from lxml import etree as ET

    def count_illu(doc):
        """
        Counts how many pages, decorations, drop capitals and figures there are in document
        :param doc: str
            Path to document
        :return: str
            Gives how many pages, decorations, drop capitals and figures there are in document
        """
   	 document_final = ET.parse(doc)
   	 racine = document_final.getroot()
   	 page = 0
   	 decoration = 0
   	 dropcapital = 0
   	 figure = 0
   	 for surfacegrp in racine[1]:
       		 page +=1
       		 for surface in surfacegrp:
           		 if surface.get('type') == 'decoration':
               			 decoration += 1
           		 elif surface.get('type') == 'dropcapital':
               			 dropcapital += 1
           		 elif surface.get('type') == 'figure':
               			 figure += 1
   	 print("page : " + str(page))
   	 print("decoration : " + str(decoration))
   	 print("dropcapital : " + str(dropcapital))
   	 print("figure : " + str(figure))
