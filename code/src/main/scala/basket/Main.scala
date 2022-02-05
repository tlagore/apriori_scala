package basket

import scala.io.Source

object Main extends App {

  def lines(filename: String) = {
    Source.fromFile(filename).getLines()
  }

  // process arguments
  if (args.size < 3 || args.size > 4) {
    args.foreach(println)
    throw new IllegalArgumentException(s"Arguments missing <filename> <delimiter> <relativeSupportThreshold> [limit] ")
  }
  val filename = args(0)
  val delim = args(1)
  if (delim.size != 1) {
    throw new IllegalArgumentException(s"Delimiter should be one character ([${delim}] provided)")
  }
  val threshold = args(2).toDouble

  val limit = if (args.size == 4) Option(args(3).toInt) else None

  System.err.println(s"Running with parameters: Filename [$filename] Separator [$delim] Minimum relative support threshold [$threshold]." + {
    limit match {
      case None => ""
      case Some(i) => s" Print at most ${i} tuples."
    }
  } + "\n")

  // do the work

  val (count, supportT, items) = aPriori.doFirstPass(threshold, lines(filename), delim)

  println(s"""${count} records, only ${items.size} item${if (items.size > 1) "s" else ""} above support threshold ${supportT} (${threshold}).""")

  val freqPairs = aPriori.doSecondPass(supportT, items, lines(filename), delim)

  println(s"""${freqPairs.size} frequent pair${if (freqPairs.size > 1) "s" else ""}""")
  val flattened = freqPairs.foldLeft(List[(Elem,Elem,Int)]())((acc, el) => acc :+ (el._1._1, el._1._2, el._2)).sortBy(_._3).filter(row => row._1 == "roses regency teacup and saucer" || row._2 == "roses regency teacup and saucer")

  flattened.foreach(println(_))


  aPriori.doResults(count, items, freqPairs, limit)


}
