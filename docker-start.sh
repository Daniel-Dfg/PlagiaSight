docker build -t plagiaeye .
docker run -itd --privileged --name PlagiaEye -p 3489:3389 plagiaeye:latest