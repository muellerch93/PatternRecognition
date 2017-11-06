# PatternRecognition

#clone project:

git clone https://github.com/muellerch93/PatternRecognition.git

#setup dependencies:

mvn install:install-file -Dfile=libs/jdom-2.0.5.jar -DgroupId=com.customlib -DartifactId=jdom -Dversion=1.0 -Dpackaging=jar

mvn install:install-file -Dfile=libs/JEvolution.jar -DgroupId=com.customlib -DartifactId=jevolution -Dversion=1.0 -Dpackaging=jar

#package and run:

mvn package

java -jar target/PatternRecognition-1.0-SNAPSHOT.jar

#or: just create new project from existing source (Idea etc.)