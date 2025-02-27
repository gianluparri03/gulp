# Gianluca's U? Library Project

GULP is a (really simple) website that can keep track of the books you own and
(maybe) you've read.

Actually, this is a proof of concept, written in Python. Maybe one day, when
it'll be finished, I'll rewrite it (perhaps in another language).

If you want you can contribute by submitting a pull request.

A more detailed documentation is coming soon, I promise.

## Running

Once you've installed the requirements (`pip install -r requirements.txt`) you
can run the server locally. In order to do it, you just have to do `make run`.
Note that this command will create a docker container where the database will be
run; otherwise, you can customize the configs file and then run
`@GULP_ENV=development python3 -c "import gulp; gulp.run()"`.

In the same way, you can run the tests with `make test`; also this command uses
the docker container.
