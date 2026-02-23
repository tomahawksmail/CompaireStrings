docker build --no-cache -t string-compare-app .
docker run -d -p 4999:4999 string-compare-app