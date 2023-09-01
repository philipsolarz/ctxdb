#!/bin/bash

# Function to display the menu
show_menu() {
  echo "1) Use In-Memory database"
  echo "2) Use Redis database"
  echo "3) Use PostgreSQL database"
  echo "4) Exit"
}

# Function to read the user's choice
read_choice() {
  read -p "Enter your choice [1-4]: " choice
}

# Function to run the Docker container
run_docker() {
  echo "Building Docker image..."
  docker build -t ctxdb-api .
  
  echo "Running Docker container..."
  docker run -p 8000:8000 -e DB_TYPE="$1" -e DB_URL="$2" ctxdb-api
}

while true; do
  # Show menu and read user's choice
  show_menu
  read_choice

  case $choice in
    1)
      echo "You chose to use the In-Memory database."
      run_docker "inmemory" ""
      break
      ;;
    2)
      echo "You chose to use the Redis database."
      read -p "Enter Redis URL (default is redis://localhost:6379/0): " redis_url
      run_docker "redis" "${redis_url:-redis://localhost:6379/0}"
      break
      ;;
    3)
      echo "You chose to use the PostgreSQL database."
      read -p "Enter PostgreSQL URL (default is postgresql://localhost/dbname): " postgres_url
      run_docker "postgres" "${postgres_url:-postgresql://localhost/dbname}"
      break
      ;;
    4)
      echo "Exiting."
      exit 0
      ;;
    *)
      echo "Invalid choice, please try again."
      ;;
  esac
done
