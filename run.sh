docker build --no-cache -t string-compare-app:1 .
docker stop comparison && docker rm comparison
docker run -d --name comparison --restart unless-stopped -p 4999:4999 string-compare-app:1