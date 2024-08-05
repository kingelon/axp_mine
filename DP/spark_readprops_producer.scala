package com.example

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import java.util.Properties
import scala.io.Source
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerConfig, ProducerRecord}

object SparkStreamingKafkaProducer {
  def main(args: Array[String]): Unit = {
    if (args.length != 2) {
      println("Usage: SparkStreamingKafkaProducer <properties-file-path> <data-file-path>")
      System.exit(1)
    }

    val propertiesFilePath = args(0)
    val dataFilePath = args(1)

    // Load properties file
    val properties = new Properties()
    properties.load(Source.fromFile(propertiesFilePath).bufferedReader())

    val kafkaBootstrapServers = properties.getProperty("kafka.bootstrap.servers")
    val kafkaTopic = properties.getProperty("kafka.topic")

    // Create a Spark session
    val spark = SparkSession.builder
      .appName("SparkStreamingKafkaProducer")
      .getOrCreate()

    import spark.implicits._

    // Read the data file
    val dataSchema = new StructType()
      .add("col1", StringType)
      .add("col2", StringType)
      .add("col3", StringType)
      .add("col4", StringType)
      .add("col5", StringType)
      .add("col6", StringType)
      .add("col7", StringType)
      .add("col8", StringType)
      .add("col9", StringType)
      .add("col10", StringType)

    val dataDF = spark.read
      .option("delimiter", "\t")
      .schema(dataSchema)
      .csv(dataFilePath)

    // Convert DataFrame to JSON string for Kafka
    val jsonDataDF = dataDF.select(to_json(struct($"*")).as("value"))

    // Create Kafka producer properties
    val props = new Properties()
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBootstrapServers)
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")

    // Create Kafka producer
    val producer = new KafkaProducer[String, String](props)

    // Send data to Kafka
    jsonDataDF.collect().foreach(row => {
      val value = row.getAs[String]("value")
      val record = new ProducerRecord[String, String](kafkaTopic, null, value)
      producer.send(record)
      println(s"Sent message: $value")
    })

    // Close the producer
    producer.close()

    spark.stop()
  }
}
