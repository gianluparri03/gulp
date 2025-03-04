<img src="gulp/web/static/logo.png">

# Gianluca's U Library Project


GULP is a (really simple) website that can keep track of the books you own and
(maybe) you've read.

If you want you can contribute by submitting a pull request.

A more detailed documentation is coming soon, I promise.

## Running

Once you've installed the requirements (`pip install -r requirements.txt`) you
can run the server locally.

In order to do it, you can just `make run`.
Note that this command will create a docker container where the database will be
run; otherwise, you can customize the configs file and then run
`GULP_ENV=development python3 -c "import gulp; gulp.run()"`.

In the same way, you can run the tests with `make test`; also this command uses
the docker container.

## Credits

The logo and the icon are made with [Inter font](https://rsms.me/inter/) and
[this icon](https://www.flaticon.com/free-icon/stack-of-books_5832416).

GULP uses [Bulma CSS](https://bulma.io).
