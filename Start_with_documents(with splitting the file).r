# getting fle and readind it line by line
fileName <- "/Users/amitbansal/Desktop/12000.txt"             # chnage the name of the file which you want to use as an input for the program
openfile <- file(fileName,open="r")
readfile <- readLines(openfile)

# checking for directory 
a0 <- "/Users/amitbansal/Desktop"            # Destination folder where you want to store or create file
a <- paste(a0,"/_123_r_work_123_123",sep="")
if(!dir.exists(a)){
  dir.create(file.path(a))
} else{
  if(dir.exists(a)){
    unlink(a, recursive=TRUE)  
    dir.create(file.path(a))
  }
}

#check for repeated word directory
a1 <- paste(a,"/repeated_words/",sep = "")
if(!dir.exists(a1)){
  dir.create(file.path(a1))
} else{
  if(dir.exists(a1)){
    unlink(a1, recursive=TRUE)  
    dir.create(file.path(a1))
  }
}

#check for word cloud directory  
a2 <- paste(a1,"/word_cloud/",sep = "")
if(!dir.exists(a2)){
  dir.create(file.path(a2))
} else{
  if(dir.exists(a2)){
    unlink(a2, recursive=TRUE)  
    dir.create(file.path(a2))
  }
}




# splitting the bigger file in small file of 5000 lines of data
b <- 0
g <- ""
for (i in 1:length(readfile)){
  if((i-1)%%5000==0){
    b <- b+1
    c <- paste(b,".txt",sep="")
    d <- paste(a,"/",sep="")
    e <- paste(d,c,sep="")
    f <- file.create(e)
    g <- file(e,open = "w")
  }
  writeLines(readfile[i],g)
}

#access each file for manupulation

noc = 20                # enter the number of topic or cluster you want to create i am creating 20 clusters and displaying the top 20 words for each topic 
twords = 20       # top words for each topic want to display

library(tm)
library(svd)
library(topicmodels)
library(lsa)
library(topsis)
library(fclust)
library(devtools)
library(irlba)
library(skmeans)
library(data.table)
library(SnowballC)
library(wordcloud)
library(RColorBrewer)


require(tm)
require(svd)
require(topicmodels)
require(lsa)
require(topsis)
require(fclust)
require(devtools)
require(irlba)
require(skmeans)
require(data.table)
require(SnowballC)
require(wordcloud)
require(RColorBrewer)

for(i in 1:b){
  h <- paste(i,".txt",sep="")
  k <- paste(d,h,sep="")
  l <- file(k,open = "r")
  m <- readLines(l)
  
  corpus <- Corpus(VectorSource(m))
  dtm <- DocumentTermMatrix(corpus, control = list(stemming = TRUE, stopwords=TRUE, minWordLength=3,removeNumbers=TRUE, removePunctuation=TRUE))
  matrix0 <- as.matrix(dtm)
  matrix1 <- matrix0
  x <- lw_logtf(matrix1)* gw_idf(matrix1)
  
  #p(w)       
  pword <- 0
  sum_of_columns <- colSums(x)
  sum_of_matrix <- sum(x)
  for(i in 1:nrow(data.matrix(sum_of_columns))){pword[i]=sum_of_columns[i]/sum_of_matrix}
  
  #p(d) probability of document
  pdoc <- 0
  no_of_documents <- nrow(matrix1)
  for(i in 1:no_of_documents){pdoc[i]=1/no_of_documents}
  
  #p(w|d)
  rows = nrow(x)
  columns = ncol(x)
  sum_of_rows = rowSums(x)
  pwgd = matrix(rep(0),nrow = rows,ncol = columns)
  for (i in 1:rows){pwgd[i,]=x[i,]/sum_of_rows[i]}
  
  #deduction technique
  dR2 <- irlba(x, 2)
  
  #clustering p(T|D)
  ptgw <- skmeans(dR2$u,k = noc, m = 1.1,control = list(nruns = 5, verbose = TRUE))  #k in the number of cluster and for accessign the matrix we need $membership
  
  #p(T,D)
  A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))
  for (i in 1:nrow(A)){A[i,] = as.matrix(ptgw$membership[i,]*pdoc[i])}
  
  #p(d|t)
  B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))
  Sum_of_columns = colSums(A)
  for (j in 1:ncol(B)){B[,j]=A[,j]/Sum_of_columns[j]}
  
  #p(w|t)
  tpwdt <- t(pwgd)
  pwgt <- tpwdt %*% B
  
  
  o <- paste(d,"Newfile.txt",sep="")
  sink(o,append=TRUE)
  for (i in 1:noc){cat ("", "",row.names(t(matrix1))[order(pwgt[,i],decreasing = TRUE)[1:20]],"\n")}
  sink()
}

# execute the algorithm again for the new file created with top topic from individual file 
p <- readLines(o)
corpus <- Corpus(VectorSource(m))
dtm <- DocumentTermMatrix(corpus, control = list(stemming = TRUE, stopwords=TRUE, minWordLength=3,removeNumbers=TRUE, removePunctuation=TRUE))
matrix0 <- as.matrix(dtm)
matrix1 <- matrix0
x <- lw_logtf(matrix1)* gw_idf(matrix1)

#p(w)       
pword <- 0
sum_of_columns <- colSums(x)
sum_of_matrix <- sum(x)
for(i in 1:nrow(data.matrix(sum_of_columns))){pword[i]=sum_of_columns[i]/sum_of_matrix}

#p(d) probability of document
pdoc <- 0
no_of_documents <- nrow(matrix1)
for(i in 1:no_of_documents){pdoc[i]=1/no_of_documents}

#p(w|d)
rows = nrow(x)
columns = ncol(x)
sum_of_rows = rowSums(x)
pwgd = matrix(rep(0),nrow = rows,ncol = columns)
for (i in 1:rows){pwgd[i,]=x[i,]/sum_of_rows[i]}

#deduction technique
dR2 <- irlba(x, 2)

#clustering p(T|D)
ptgw <- skmeans(dR2$u,k = noc, m = 1.1,control = list(nruns = 5, verbose = TRUE))  #k in the number of cluster and for accessign the matrix we need $membership

#p(T,D)
A = matrix(rep(0), nrow = nrow(ptgw$membership), ncol = ncol(ptgw$membership))
for (i in 1:nrow(A)){A[i,] = as.matrix(ptgw$membership[i,]*pdoc[i])}

#p(d|t)
B = matrix(rep(0),nrow=nrow(A),ncol = ncol(A))
Sum_of_columns = colSums(A)
for (j in 1:ncol(B)){B[,j]=A[,j]/Sum_of_columns[j]}

#p(w|t)
tpwdt <- t(pwgd)
pwgt <- tpwdt %*% B

q <- paste(d,"Topwords.txt",sep="")
sink(q,append=TRUE)
for (i in 1:noc){cat ("", "",row.names(t(matrix1))[order(pwgt[,i],decreasing = TRUE)[1:20]],"\n")}
sink()

# Repeat the word for wordcloud of the top words
r <- readLines(q)
for(i in 1:length(r)){
  s <- trimws(r[i])
  s1 <- paste("topic ", toString(i)," - ",s,sep = "")
  print(s1)
  t <- unlist(strsplit(s," "))
  r1 <- length(t)
  r2 <- 1
  t1 <- paste("repeated_word_topc_",i,".txt", sep = "")
  t2 <- paste(a1,t1,sep="")
  t3 <- file.create(t2)
  for(j in 1:length(t)){
    sink(t2,append=TRUE)
    u <- replicate(r1,t[j])
    v <- cat(u,"\n")
    sink()
    r1 <- r1 - 1
    r2 <- r2 + 1
  }
  w1 <- paste("word_cloud_topic_",i,".png", sep = "")
  w2 <- paste(a2,w1,sep="")
  w3 <- file.create(w2)
  text <- readLines(t2)
  docs <- Corpus(VectorSource(text))      #Load the data as a corpus
  #docs <- tm_map(docs, removeWords, stopwords("english")) # Remove english common stopwords
  #docs <- tm_map(docs, stripWhitespace)  #Eliminate extra white spaces
  dtm <- TermDocumentMatrix(docs) 
  m <- as.matrix(dtm) 
  v <- sort(rowSums(m),decreasing=TRUE) 
  d <- data.frame(word = names(v),freq=v) 
  #print(head(d,20))
  set.seed(1234)
  wordcloud(words = d$word, freq = d$freq, min.freq = 1, max.words=200, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"))            
  png(w2, width=1280,height=800)
  wordcloud(words = d$word, freq = d$freq, min.freq = 1, max.words=200, random.order=FALSE, rot.per=0.35, colors=brewer.pal(8, "Dark2"))            
}



