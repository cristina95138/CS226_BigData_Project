from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql import functions as F
#from textblob import TextBlob

def preprocess(df):
    df = df.drop("_c0")
    df = df.drop("_c3")
    df = df.drop("_c4")
    df = df.drop("_c5")
    df = df.drop("_c6")
    df = df.drop("_c7")
    df = df.withColumnRenamed("_c1", "text")
    df = df.withColumnRenamed("_c2", "geo")
    df = df.withColumnRenamed("_c8", "brand")
    df = df.filter(df.text != "text")

    return df

# text classification
def polarity_detection(text):
    return TextBlob(text).sentiment.polarity
def subjectivity_detection(text):
    return TextBlob(text).sentiment.subjectivity
def text_classification(words):
    # polarity detection
    polarity_detection_udf = udf(polarity_detection, StringType())
    words = words.withColumn("polarity", polarity_detection_udf("word"))
    # subjectivity detection
    subjectivity_detection_udf = udf(subjectivity_detection, StringType())
    words = words.withColumn("subjectivity", subjectivity_detection_udf("word"))
    return words


if __name__ == "__main__":
    # create Spark session
    spark = SparkSession.builder.appName("TwitterSentimentAnalysis").getOrCreate()
    # read the tweet data from socket
    df = spark.read.csv("Data/Preprocessed Tweets/*.csv", multiLine=True)
    df = preprocess(df)
    df.printSchema()
    df.show()
    # # Preprocess the data
    # words = preprocessing(lines)
    # # text classification to define polarity and subjectivity
    # words = text_classification(words)
    # words = words.repartition(1)
    # query = words.writeStream.queryName("all_tweets")\
    #     .outputMode("append").format("parquet")\
    #     .option("path", "./parc")\
    #     .option("checkpointLocation", "./check")\
    #     .trigger(processingTime='60 seconds').start()
    # query.awaitTermination()