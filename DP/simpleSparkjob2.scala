package com.example

import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import java.util.Properties
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerConfig, ProducerRecord}
import java.util.UUID

object ContinuousKafkaProducer {
  def main(args: Array[String]): Unit = {
    // Kafka configuration
    val kafkaBootstrapServers = "server1:5660,server2:5660,server3:5660"
    val kafkaTopic = "/mapr/streams/path_to_stream:input"

    // Create a Spark session
    val spark = SparkSession.builder
      .appName("ContinuousKafkaProducer")
      .getOrCreate()

    import spark.implicits._

    // Create Kafka producer properties
    val props = new Properties()
    props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, kafkaBootstrapServers)
    props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")
    props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, "org.apache.kafka.common.serialization.StringSerializer")

    // Create Kafka producer
    val producer = new KafkaProducer[String, String](props)

    try {
      // Generate and send sample data continuously
      while (true) {
        val key = UUID.randomUUID().toString
        val value = "Sample message " + UUID.randomUUID().toString
        val record = new ProducerRecord[String, String](kafkaTopic, key, value)
        
        producer.send(record)
        println(s"Sent message: $key -> $value")
        
        Thread.sleep(1000) // Sleep to simulate real-time data generation
      }
    } catch {
      case e: Exception => e.printStackTrace()
    } finally {
      // Close the producer after use
      producer.close()
    }

    spark.stop()
  }
}
