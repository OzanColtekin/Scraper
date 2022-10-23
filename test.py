from Database import Database
import pandas as pd
import main
import schedule
import time


catDf=pd.read_csv("categories.csv")
names=catDf.name.values.tolist()
catID = 1324
main.Trendyol("Robot Süpürge",catID).start_schedules()


while True:
    schedule.run_pending()
    time.sleep(5)