setwd("C:/Users/00811289/Documents/github/trip-advisor-scrapers/downloadedhotels")
train <- read.csv("file.csv")

write.csv(train, file="cleaned.csv",sep=",", na = "NA")
