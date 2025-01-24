 #!usr/bin/env bash
 
 
echo "\033[36m ======================= Sustainability Local Setup ==========================\033[0m"
read -p "Is Docker in Running State :(Y / N)" running
echo "\033[0m"

if [ "$running" == "Y" ]  || [ "$running" == "y" ]; then
    echo "\033[36m =======================   building image ========================\033[0m"
   docker compose  -f docker-composer-local.yml build
    
     echo "\033[36m =======================   building image completed ========================\033[0m"
      echo "\033[36m =======================   starting sust-backend-api ========================\033[0m"
   
   docker compose  -f docker-composer-local.yml up
    
   
     
else
    echo "\033[31mPlease start your docker!. then execute same command.\033[0m"
fi
#docker build -t sust-backend-api .
#docker run -it sust-backend-api