package org.foo.bar

object Main extends App {

  println("-- avdl example --")
  val person = new Person(System.currentTimeMillis(), "Arron", "Green")
  println(s"${person}")
  
  println("-- avsc example --")
  val user = new User("Arron", Some(3), Some("green"))
  println(s"${user}")

}
