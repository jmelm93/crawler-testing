# docker kill all running containers
docker kill $(docker ps -a -q)

# docker image build local compuet
docker build -t swf_crawlers .

# launch in background
# -d = detached
# -p = port
# docker run on local host
docker run -d --network='host' swf_crawlers

# docker list ALL running containers
docker ps -a

