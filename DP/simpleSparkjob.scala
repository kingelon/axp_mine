import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import java.util.UUID

object SimpleKafkaProducer {
  def main(args: Array[String]): Unit = {
    // Create a Spark session
    val spark = SparkSession.builder
      .appName("SimpleKafkaProducer")
      .getOrCreate()

    import spark.implicits._

    // Create a DataFrame with sample data
    val sampleData = Seq(
      (UUID.randomUUID().toString, "Sample message 1"),
      (UUID.randomUUID().toString, "Sample message 2"),
      (UUID.randomUUID().toString, "Sample message 3")
    ).toDF("key", "value")

    // Write the DataFrame to Kafka
    sampleData.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")
      .write
      .format("kafka")
      .option("kafka.bootstrap.servers", "your_kafka_cluster:9092")
      .option("topic", "test-topic")
      .save()

    spark.stop()
  }
}
