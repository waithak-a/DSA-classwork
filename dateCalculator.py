class DateCalculator:

    def __init__(self, year: int, month: int, day:int):
        self.year = year
        self.month = month
        self.day = day
        self.days = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        
    def adjust_for_jan_and_feb(self):
        if self.month < 3:
            self.month +=12
            self.year -= 1
                
    def calculate_components(self):
            k = self.year % 100
            j = self.year// 100
            return k,j
    def zellers_congruence(self):
            self.adjust_for_jan_and_feb()
            k,j = self.calculate_components()
                    
            q=self.day
            m=self.month
                    
            h= (q+ (13*(m + 1))//5 + k + (k//4) + (j//4) + 5*j)
            h %= 7
            return self.days[h]
                
    def get_days(self):
            return self.zellers_congruence()
                
    def print_result(self):
            day = self.get_days()
            print(f"{self.month if self.month <= 12 else self.month-12}/{self.day}/{self.year} falls on a {day}")

if __name__ == "__main__":
    norm_date = DateCalculator(year = int(input("Enter year: ")), month = int(input("Enter month: ")), day = int(input("Enter day: ")))
    print("The date is:")
    norm_date.print_result()

# other example dates that will be outputted
for year, month, day in [(2005, 11, 5), (2024, 10, 7), (2014, 12, 9)]:
    calculator = DateCalculator(year, month, day)
    print(f"{day}/{month}/{year} falls on a {calculator.get_days()}")