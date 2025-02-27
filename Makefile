DB_CONTAINER_NAME = gulp_db
DB_USERNAME = gulp
DB_PASSWORD = gulp
DB_DEV_DB = gulp
DB_TEST_DB = test


# Makes sure that the database is running
start_db:
	@if [ "$(shell docker ps -a -q -f name=$(DB_CONTAINER_NAME))" ]; then \
		if [ ! "$(shell docker ps -aq -f status='running' -f name=$(DB_CONTAINER_NAME))" ]; then \
			docker start $(DB_CONTAINER_NAME); \
		fi \
	else \
		docker run -d --name $(DB_CONTAINER_NAME) \
		-e POSTGRES_USER=$(DB_USERNAME) \
		-e POSTGRES_PASSWORD=$(DB_PASSWORD) \
		-e POSTGRES_DB=$(DB_DEV_DB) \
		-p 5432:5432 postgres; \
	fi


# Drops the database entirely
drop_db:
	@docker stop $(DB_CONTAINER_NAME)
	@docker rm $(DB_CONTAINER_NAME)

# Opens a shell with the database
dbsh: start_db
	@docker exec -it $(DB_CONTAINER_NAME) psql -U $(DB_USERNAME) -d $(DB_DEV_DB)

# Runs the webserver
run: start_db
	@GULP_ENV=development python3 -c "import gulp; gulp.run()"

# Runs the tests
test: start_db
	@-docker exec -it $(DB_CONTAINER_NAME) dropdb -U $(DB_USERNAME) "$(DB_TEST_DB)"
	@docker exec -it $(DB_CONTAINER_NAME) createdb -U $(DB_USERNAME) "$(DB_TEST_DB)"
	@GULP_ENV=testing python3 -m unittest gulp.database.tests
