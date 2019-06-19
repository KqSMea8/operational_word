#!/bin/bash

PROJECT_NAME=$1
/app/jdk1.8.0_45/bin/java -jar /app/jar/www/${PROJECT_NAME}/${PROJECT_NAME}.jar -vmargs -Xms1024M -Xmx2048M -XX:PermSize=256M -XX:MaxPermSize=256M  --spring.profiles.active=produce  >/app/jar/logs/${PROJECT_NAME}.log 2>&1 &
