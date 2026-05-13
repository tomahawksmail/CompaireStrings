docker stack rm comparison
docker build --no-cache -t string-compare-app:1 .
docker tag string-compare-app:1 dregistrygui.uskoinc.com/string-compare-app:1
docker push dregistrygui.uskoinc.com/string-compare-app:1
docker stack deploy -c service.yml comparison