/app/jdk1.8.0_45/bin/java -Xms2g -Xmx2g -XX:PermSize=256m -XX:MaxPermSize=256m -Dspring.profiles.active=test -jar /app/jar/ROOT/tamc-cloud-h5.jar >/app/jar/logs/tamc-cloud-h5.log 2>&1 &
--java自带日志分割
/app/jdk1.8.0_45/bin/java -jar  /app/jar/ROOT/interface-demo-test.jar >/app/jar/logs/interface-demo-test.log 2>&1 &

