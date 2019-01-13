from prettytable import PrettyTable

class Table:
    def __init__(self, data):
        self.__data = data
        self.t = PrettyTable(['COMPANY', 'ACCOUNT', 'PASSWORD'])

        self.t.align['COMPANY'] = 'l'
        self.t.align['PASSWORD'] = 'r'

    def clear(self):
        self.t.clear_rows()
    
    def create(self):
        self.clear()

        new_row = []
        for index, value in enumerate(self.__data):
            new_row.append(value)

            if len(new_row) == 3:
                self.t.add_row(new_row)
                new_row = []
            
        return self.t

    # def create_by_company(self):
        

    def filter_columns(self, filter):
        self.clear()
        self.create()
        
        filtered = self.t.get_string(fields=filter)
        return filtered