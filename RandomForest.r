library("randomForest", help, pos = 2, lib.loc = NULL)

ts <- read.table("input.ML.matrix", header = T, row.names = 1)
ts_d <- as.data.frame(ts)
index <- sample(2, nrow(ts_d), replace = T, prob = c(0.7,0.3))
traindata <- ts_d[index==1,]
testdata <- ts_d[index==2,]
n <- ncol(ts_d) - 1
errRate <- c(1)
for (i in 1:n){
    m <- randomForest(Invade~.,data=ts_d,mtry=i,proximity=TRUE)
    err<-mean(m$err.rate)
    errRate[i] <- err
}
m= which.min(errRate)
print(m)
rf_ntree <- randomForest(Invade~.,data=ts_d)
pdf(file = "rf_ntree.pdf")
plot(rf_ntree)
dev.off()
